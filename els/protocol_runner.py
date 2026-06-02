"""Run fixed Open Bible Codes protocol files."""

from __future__ import annotations

import json
import hashlib
import os
import subprocess
import sys
import time
import tomllib
from concurrent.futures import FIRST_COMPLETED, Future, ThreadPoolExecutor, wait
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
STEP_STAMP_VERSION = 2


def load_protocol(path: str | Path) -> dict[str, Any]:
    protocol_path = Path(path).expanduser().resolve()
    with protocol_path.open("rb") as handle:
        protocol = tomllib.load(handle)
    _validate_protocol(protocol, protocol_path)
    protocol["__path__"] = str(protocol_path)
    return protocol


def run_protocol(
    path: str | Path,
    *,
    only: set[str] | None = None,
    dry_run: bool = False,
    manifest_out: str | Path | None = None,
    resume: bool = False,
) -> int:
    protocol = load_protocol(path)
    steps = _selected_steps(protocol, only)
    manifest_path = Path(
        manifest_out
        or protocol.get("manifest_out")
        or "reports/protocol_run.manifest.json"
    )
    if not manifest_path.is_absolute():
        manifest_path = ROOT / manifest_path
    stamp_dir = manifest_path.parent / ".step-stamps"

    run = {
        "tool": "run_protocol",
        "protocol": protocol.get("name", ""),
        "description": protocol.get("description", ""),
        "protocol_path": protocol["__path__"],
        "started_utc": datetime.now(UTC).isoformat(),
        "cwd": str(ROOT),
        "dry_run": dry_run,
        "steps": [],
        "status": "running",
    }

    protocol_started = time.monotonic()
    exit_code = 0
    for step_group in grouped_steps(steps):
        if len(step_group) == 1:
            step_result = run_step(
                step_group[0],
                dry_run=dry_run,
                resume=resume,
                capture_output=False,
                stamp_dir=stamp_dir,
            )
            step_records = [step_result["record"]]
        else:
            step_records = run_parallel_step_group(
                step_group,
                dry_run=dry_run,
                resume=resume,
                max_workers=parallel_workers(protocol),
                progress_interval=progress_interval_seconds(protocol),
                stamp_dir=stamp_dir,
            )

        run["steps"].extend(step_records)
        failed_step = first_failed_step(step_records, step_group)
        if failed_step is not None:
            run["status"] = "failed"
            exit_code = int(failed_step["return_code"])
            break
    else:
        run["status"] = "success"

    run["ended_utc"] = datetime.now(UTC).isoformat()
    run["duration_seconds"] = round(time.monotonic() - protocol_started, 3)
    run["timing_summary"] = timing_summary(run["steps"])
    if not dry_run:
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        atomic_write_text(
            manifest_path,
            json.dumps(run, ensure_ascii=False, indent=2) + "\n",
        )
        print_timing_summary(run["timing_summary"])
        try:
            print(manifest_path.relative_to(ROOT))
        except ValueError:
            print(manifest_path)
    return exit_code


def timing_summary(steps: list[dict[str, Any]]) -> dict[str, Any]:
    total_step_seconds = round(
        sum(float(step.get("duration_seconds", 0.0)) for step in steps),
        3,
    )
    step_timings = [
        {
            "id": step["id"],
            "duration_seconds": step.get("duration_seconds", 0.0),
            "skipped": step.get("skipped", False),
            "return_code": step.get("return_code"),
        }
        for step in steps
    ]
    return {
        "total_step_seconds": total_step_seconds,
        "ran_steps": sum(1 for step in step_timings if not step["skipped"]),
        "skipped_steps": sum(1 for step in step_timings if step["skipped"]),
        "slowest_steps": sorted(
            step_timings,
            key=lambda step: float(step["duration_seconds"]),
            reverse=True,
        ),
    }


def print_timing_summary(summary: dict[str, Any]) -> None:
    print("== timing ==", flush=True)
    for step in summary.get("slowest_steps", []):
        status = "cached" if step.get("skipped") else f"rc={step.get('return_code')}"
        print(f"{step['duration_seconds']:>8.3f}s {step['id']} {status}", flush=True)


def run_step(
    step: dict[str, Any],
    *,
    dry_run: bool,
    resume: bool,
    capture_output: bool,
    stamp_dir: Path,
) -> dict[str, Any]:
    command = _command_for_step(step)
    step_record = {
        "id": step["id"],
        "description": step.get("description", ""),
        "command": command,
        "inputs": step.get("inputs", []),
        "outputs": step.get("outputs", []),
        "always_run": bool(step.get("always_run", False)),
        "parallel_group": step.get("parallel_group", ""),
        "started_utc": datetime.now(UTC).isoformat(),
    }
    if not capture_output:
        print(f"== {step['id']} ==", flush=True)
        print(" ".join(command), flush=True)
    started = time.monotonic()
    stdout = ""
    stderr = ""
    if (
        resume
        and not bool(step.get("always_run", False))
        and step_outputs_current(step, command, stamp_dir)
    ):
        if not capture_output:
            print("cached", flush=True)
        return_code = 0
        skipped = True
    elif dry_run:
        return_code = 0
        skipped = False
    else:
        completed = subprocess.run(
            command,
            cwd=ROOT,
            check=False,
            capture_output=capture_output,
            text=capture_output,
        )
        return_code = completed.returncode
        skipped = False
        if capture_output:
            stdout = completed.stdout or ""
            stderr = completed.stderr or ""
        if return_code == 0 and step.get("outputs") and not step_outputs_exist(step):
            return_code = 2
            message = f"missing expected output(s): {', '.join(missing_outputs(step))}\n"
            if capture_output:
                stderr += message
            else:
                print(message, end="", file=sys.stderr, flush=True)
        if return_code == 0:
            write_step_stamp(step, command, stamp_dir)
    step_record["ended_utc"] = datetime.now(UTC).isoformat()
    step_record["duration_seconds"] = round(time.monotonic() - started, 3)
    step_record["return_code"] = return_code
    step_record["skipped"] = skipped
    return {"record": step_record, "stdout": stdout, "stderr": stderr}


def run_parallel_step_group(
    steps: list[dict[str, Any]],
    *,
    dry_run: bool,
    resume: bool,
    max_workers: int,
    progress_interval: float,
    stamp_dir: Path,
) -> list[dict[str, Any]]:
    group_name = str(steps[0].get("parallel_group", ""))
    print(
        f"== parallel group {group_name} ({len(steps)} steps, max {max_workers}) ==",
        flush=True,
    )
    for step in steps:
        print(f"== {step['id']} ==", flush=True)
        print(" ".join(_command_for_step(step)), flush=True)

    records_by_id: dict[str, dict[str, Any]] = {}
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(
                run_step,
                step,
                dry_run=dry_run,
                resume=resume,
                capture_output=True,
                stamp_dir=stamp_dir,
            ): step
            for step in steps
        }
        submitted_at = {future: time.monotonic() for future in futures}
        pending: set[Future[dict[str, Any]]] = set(futures)
        last_progress = time.monotonic()
        while pending:
            completed, pending = wait(
                pending,
                timeout=progress_timeout(progress_interval, last_progress),
                return_when=FIRST_COMPLETED,
            )
            if not completed:
                now = time.monotonic()
                print_parallel_progress(futures, pending, submitted_at, now)
                last_progress = now
                continue
            last_progress = time.monotonic()
            for future in completed:
                step = futures[future]
                result = future.result()
                records_by_id[step["id"]] = result["record"]
                print_parallel_step_output(step, result)

    return [records_by_id[step["id"]] for step in steps]


def progress_timeout(progress_interval: float, last_progress: float) -> float | None:
    if progress_interval <= 0:
        return None
    return max(0.0, progress_interval - (time.monotonic() - last_progress))


def print_parallel_progress(
    futures: dict[Future[dict[str, Any]], dict[str, Any]],
    pending: set[Future[dict[str, Any]]],
    submitted_at: dict[Future[dict[str, Any]], float],
    now: float,
) -> None:
    active = [
        (futures[future]["id"], now - submitted_at[future])
        for future in pending
    ]
    if active:
        print(format_parallel_progress(active), flush=True)


def format_parallel_progress(active: list[tuple[str, float]]) -> str:
    active_steps = ", ".join(
        f"{step_id} {duration:.1f}s"
        for step_id, duration in sorted(active)
    )
    return f"== progress active: {active_steps} =="


def print_parallel_step_output(step: dict[str, Any], result: dict[str, Any]) -> None:
    record = result["record"]
    status = "cached" if record.get("skipped") else f"rc={record['return_code']}"
    print(
        f"== {step['id']} done {record['duration_seconds']:.3f}s {status} ==",
        flush=True,
    )
    stdout = result.get("stdout", "")
    stderr = result.get("stderr", "")
    if stdout:
        print(stdout, end="" if stdout.endswith("\n") else "\n", flush=True)
    if stderr:
        print(stderr, end="" if stderr.endswith("\n") else "\n", file=sys.stderr, flush=True)


def grouped_steps(steps: list[dict[str, Any]]) -> list[list[dict[str, Any]]]:
    groups: list[list[dict[str, Any]]] = []
    index = 0
    while index < len(steps):
        step = steps[index]
        group_name = step.get("parallel_group")
        if not group_name:
            groups.append([step])
            index += 1
            continue
        group = [step]
        index += 1
        while index < len(steps) and steps[index].get("parallel_group") == group_name:
            group.append(steps[index])
            index += 1
        groups.append(group)
    return groups


def parallel_workers(protocol: dict[str, Any]) -> int:
    raw = protocol.get("max_parallel", 1)
    if not isinstance(raw, int) or raw < 1:
        raise ValueError("max_parallel must be an integer >= 1")
    return raw


def progress_interval_seconds(protocol: dict[str, Any]) -> float:
    raw = protocol.get("progress_interval_seconds", 30)
    if not isinstance(raw, (int, float)) or raw < 0:
        raise ValueError("progress_interval_seconds must be a number >= 0")
    return float(raw)


def first_failed_step(
    records: list[dict[str, Any]],
    steps: list[dict[str, Any]],
) -> dict[str, Any] | None:
    steps_by_id = {step["id"]: step for step in steps}
    for record in records:
        step = steps_by_id[record["id"]]
        if record["return_code"] != 0 and not bool(step.get("allow_failure", False)):
            return record
    return None


def _validate_protocol(protocol: dict[str, Any], path: Path) -> None:
    if not protocol.get("name"):
        raise ValueError(f"{path}: missing protocol name")
    max_parallel = protocol.get("max_parallel", 1)
    if not isinstance(max_parallel, int) or max_parallel < 1:
        raise ValueError(f"{path}: max_parallel must be an integer >= 1")
    progress_interval = protocol.get("progress_interval_seconds", 30)
    if not isinstance(progress_interval, (int, float)) or progress_interval < 0:
        raise ValueError(f"{path}: progress_interval_seconds must be a number >= 0")
    steps = protocol.get("steps")
    if not isinstance(steps, list) or not steps:
        raise ValueError(f"{path}: expected at least one [[steps]] item")
    seen: set[str] = set()
    for index, step in enumerate(steps, start=1):
        step_id = step.get("id")
        if not isinstance(step_id, str) or not step_id:
            raise ValueError(f"{path}: step {index} missing id")
        if step_id in seen:
            raise ValueError(f"{path}: duplicate step id: {step_id}")
        seen.add(step_id)
        argv = step.get("argv")
        if not isinstance(argv, list) or not all(isinstance(item, str) for item in argv):
            raise ValueError(f"{path}: step {step_id} needs argv string list")
        parallel_group = step.get("parallel_group", "")
        if not isinstance(parallel_group, str):
            raise ValueError(f"{path}: step {step_id} parallel_group must be a string")
        inputs = step.get("inputs", [])
        if not isinstance(inputs, list) or not all(isinstance(item, str) for item in inputs):
            raise ValueError(f"{path}: step {step_id} inputs must be a string list")
        outputs = step.get("outputs", [])
        if not isinstance(outputs, list) or not all(isinstance(item, str) for item in outputs):
            raise ValueError(f"{path}: step {step_id} outputs must be a string list")
        always_run = step.get("always_run", False)
        if not isinstance(always_run, bool):
            raise ValueError(f"{path}: step {step_id} always_run must be a boolean")
        allow_failure = step.get("allow_failure", False)
        if not isinstance(allow_failure, bool):
            raise ValueError(f"{path}: step {step_id} allow_failure must be a boolean")
        python = step.get("python", True)
        if not isinstance(python, bool):
            raise ValueError(f"{path}: step {step_id} python must be a boolean")


def _selected_steps(protocol: dict[str, Any], only: set[str] | None) -> list[dict[str, Any]]:
    steps = protocol["steps"]
    if not only:
        return steps
    selected = [step for step in steps if step["id"] in only]
    missing = sorted(only - {step["id"] for step in selected})
    if missing:
        raise ValueError(f"unknown protocol step(s): {', '.join(missing)}")
    return selected


def _command_for_step(step: dict[str, Any]) -> list[str]:
    argv = [str(item) for item in step["argv"]]
    if bool(step.get("python", True)):
        return [sys.executable, *normalize_python_argv(argv)]
    return argv


def normalize_python_argv(argv: list[str]) -> list[str]:
    if not argv:
        return argv
    script = Path(argv[0])
    if (
        script.suffix == ".py"
        and len(script.parts) == 2
        and script.parts[0] == "scripts"
    ):
        return ["-m", f"scripts.{script.stem}", *argv[1:]]
    return argv


def step_outputs_exist(step: dict[str, Any]) -> bool:
    outputs = step.get("outputs", [])
    if not outputs:
        return False
    return all(_resolve_output(output).exists() for output in outputs)


def missing_outputs(step: dict[str, Any]) -> list[str]:
    return [
        str(_resolve_output(output))
        for output in step.get("outputs", [])
        if not _resolve_output(output).exists()
    ]


def step_outputs_current(
    step: dict[str, Any],
    command: list[str],
    stamp_dir: Path,
) -> bool:
    if not step_outputs_exist(step):
        return False
    if not step_inputs_exist(step):
        return False
    stamp_path = step_stamp_path(stamp_dir, step["id"])
    if not stamp_path.exists():
        return False
    try:
        stamp = json.loads(stamp_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    if not isinstance(stamp, dict):
        return False
    if stamp.get("version") != STEP_STAMP_VERSION:
        return False
    if stamp.get("command") != command:
        return False
    if stamp.get("inputs") != input_fingerprints(step):
        return False
    return stamp.get("outputs") == output_fingerprints(step)


def write_step_stamp(step: dict[str, Any], command: list[str], stamp_dir: Path) -> None:
    outputs = step.get("outputs", [])
    if not outputs or not step_outputs_exist(step) or not step_inputs_exist(step):
        return
    stamp = {
        "version": STEP_STAMP_VERSION,
        "step_id": step["id"],
        "command": command,
        "inputs": input_fingerprints(step),
        "outputs": output_fingerprints(step),
        "written_utc": datetime.now(UTC).isoformat(),
    }
    atomic_write_text(
        step_stamp_path(stamp_dir, step["id"]),
        json.dumps(stamp, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
    )


def output_fingerprints(step: dict[str, Any]) -> list[dict[str, Any]]:
    return path_fingerprints(step.get("outputs", []))


def input_fingerprints(step: dict[str, Any]) -> list[dict[str, Any]]:
    return path_fingerprints(expanded_input_paths(step))


def path_fingerprints(raw_paths: list[str]) -> list[dict[str, Any]]:
    return [path_fingerprint(path) for path in raw_paths]


def path_fingerprint(raw_path: str) -> dict[str, Any]:
    path = _resolve_output(raw_path)
    stat = path.stat()
    fingerprint: dict[str, Any] = {
        "path": str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path),
        "mtime_ns": stat.st_mtime_ns,
    }
    if path.is_file():
        fingerprint.update(
            {
                "type": "file",
                "size": stat.st_size,
                "sha256": sha256_file(path),
            }
        )
    elif path.is_dir():
        directory = directory_digest(path)
        fingerprint.update(
            {
                "type": "directory",
                "entries": directory["entries"],
                "tree_sha256": directory["tree_sha256"],
                "legacy_tree_sha256": directory["legacy_tree_sha256"],
            }
        )
    else:
        fingerprint["type"] = "other"
    return fingerprint


def step_inputs_exist(step: dict[str, Any]) -> bool:
    return all(_resolve_output(input_path).exists() for input_path in expanded_input_paths(step))


def expanded_input_paths(step: dict[str, Any]) -> list[str]:
    paths: list[str] = []
    seen: set[str] = set()
    for raw_path in step.get("inputs", []):
        for path in [raw_path, *inferred_corpus_source_inputs(raw_path)]:
            resolved = _resolve_output(str(path))
            key = str(resolved)
            if key in seen:
                continue
            seen.add(key)
            paths.append(str(path))
    return paths


def inferred_corpus_source_inputs(raw_path: str) -> list[str]:
    path = _resolve_output(raw_path)
    if path.suffix != ".toml" or not path.exists():
        return []
    try:
        with path.open("rb") as handle:
            config = tomllib.load(handle)
    except (OSError, tomllib.TOMLDecodeError):
        return []
    sources = config.get("sources", [])
    if not isinstance(sources, list):
        return []
    inferred: list[str] = []
    for source in sources:
        if not isinstance(source, dict) or not isinstance(source.get("path"), str):
            continue
        inferred.append(str(resolve_config_path(path.parent, source["path"])))
    return inferred


def resolve_config_path(base_dir: Path, raw_path: str) -> Path:
    path = Path(raw_path).expanduser()
    if path.is_absolute():
        return path
    return (base_dir / path).resolve()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def directory_digest(path: Path) -> dict[str, Any]:
    """Fingerprint a directory tree by names, entry kinds, and file contents."""

    entries: list[dict[str, Any]] = []
    legacy_entries: list[dict[str, Any]] = []
    for child in sorted(path.rglob("*")):
        stat = child.stat()
        entry: dict[str, Any] = {
            "path": str(child.relative_to(path)),
            "type": "directory" if child.is_dir() else "file",
        }
        legacy_entry = {
            **entry,
            "mtime_ns": stat.st_mtime_ns,
        }
        if child.is_file():
            entry["size"] = stat.st_size
            entry["sha256"] = sha256_file(child)
            legacy_entry["size"] = stat.st_size
        entries.append(entry)
        legacy_entries.append(legacy_entry)
    encoded = json.dumps(entries, sort_keys=True, separators=(",", ":")).encode("utf-8")
    legacy_encoded = json.dumps(
        legacy_entries,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return {
        "entries": len(entries),
        "tree_sha256": hashlib.sha256(encoded).hexdigest(),
        "legacy_tree_sha256": hashlib.sha256(legacy_encoded).hexdigest(),
    }


def step_stamp_path(stamp_dir: Path, step_id: str) -> Path:
    safe_id = "".join(
        char if char.isalnum() or char in "._-" else "_"
        for char in step_id
    )
    return stamp_dir / f"{safe_id}.json"


def atomic_write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    tmp_path.write_text(text, encoding="utf-8")
    os.replace(tmp_path, path)


def _resolve_output(output: str) -> Path:
    path = Path(output)
    if path.is_absolute():
        return path
    return ROOT / path
