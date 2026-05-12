# Partition Worker Workflow

Dense full-span partition exports are independent. Multiple machines can
process non-overlapping partition IDs, then return compressed artifacts to one
coordinator checkout.

## Roles

- Coordinator: this machine owns report regeneration, docs, commits, and pushes.
- Workers: other machines run assigned partition IDs only, compress outputs, and
  export result bundles.

Workers should not commit or push. They only return bundles.

## Coordinator: Create Assignments

```bash
python3 -m scripts.plan_partition_worker_batches --workers 3 --max-estimated-hits 1000000
```

For unequal machines, add relative speed weights. Higher weights receive a
larger share of the remaining estimated hits while still keeping partitions
non-overlapping:

```bash
python3 -m scripts.plan_partition_worker_batches \
  --workers 3 \
  --worker-weight worker_01=2.0 \
  --worker-weight worker_02=1.0 \
  --worker-weight worker_03=0.5 \
  --max-estimated-hits 1000000
```

Example use: fast Mac = `worker_01=2.0`, Windows desktop = `worker_02=1.0`,
slower laptop = `worker_03=0.5`. Re-run the planner only after importing or
marking completed results, so the next assignment is based on genuinely
remaining coordinator work.

Do not restart an old worker assignment after the coordinator has continued
locally or imported another machine's results. A stale `worker_NN_partitions.csv`
can still run successfully on the worker, but it may only duplicate partitions
that the coordinator already has archived. Before relaunching a worker, regenerate
assignments on the coordinator and send the worker its fresh `worker_NN_*` files.
If the planner reports zero selected rows, the partition queue is already complete
from the coordinator's point of view.

Outputs:

- `reports/dynamic_skip_focus/worker_batches/partition_worker_assignments.csv`
- `reports/dynamic_skip_focus/worker_batches/worker_01_partitions.csv`
- `reports/dynamic_skip_focus/worker_batches/worker_01_counts.csv`
- `reports/dynamic_skip_focus/worker_batches/worker_02_partitions.csv`
- `reports/dynamic_skip_focus/worker_batches/worker_02_counts.csv`
- `reports/dynamic_skip_focus/worker_batches/worker_03_partitions.csv`
- `reports/dynamic_skip_focus/worker_batches/worker_03_counts.csv`
- one README per worker with exact commands

Copy each worker's `worker_NN_partitions.csv` and `worker_NN_counts.csv` to
that worker machine, or copy the full `worker_batches/` directory. Keep those
files at the same repo-relative path inside the worker checkout.

## Worker: Run Assigned Partitions

From the worker checkout on its external SSD:

Prerequisites on Windows:

- Python 3.11+ available as `python`.
- Git checkout on the USB-C SSD.
- A C++17 compiler available as `clang++` or `g++`, or set `CXX` to the compiler
  command before running. The dense exporter builds a local helper binary.

```bash
python3 -m scripts.bootstrap_public_sources
python3 -m scripts.run_dynamic_span_partitions --plan reports/dynamic_skip_focus/worker_batches/worker_02_partitions.csv --partition-id-file reports/dynamic_skip_focus/worker_batches/worker_02_partitions.csv --max-estimated-hits 1000000
python3 -m scripts.summarize_dynamic_span_partition_outputs --plan reports/dynamic_skip_focus/worker_batches/worker_02_partitions.csv
python3 -m scripts.compress_dynamic_span_partition_outputs --plan reports/dynamic_skip_focus/worker_batches/worker_02_partitions.csv
python3 -m scripts.export_partition_worker_bundle --plan reports/dynamic_skip_focus/worker_batches/worker_02_partitions.csv --assignment reports/dynamic_skip_focus/worker_batches/worker_02_partitions.csv --out reports/dynamic_skip_focus/worker_batches/worker_02_results.zip
```

On Windows, use `python` instead of `python3` if that is how Python is
installed. The worker-specific plan points at the worker-specific counts CSV,
so fresh clones do not need the coordinator's ignored count reports.

## Coordinator: Import Results

Copy each worker result zip to the coordinator, then import:

```bash
python3 -m scripts.import_partition_worker_bundle worker_02_results.zip
python3 -m scripts.import_partition_worker_bundle worker_03_results.zip
python3 -m scripts.summarize_dynamic_span_partition_outputs
python3 -m scripts.compare_completed_dense_partitions
python3 -m scripts.compress_dynamic_span_partition_outputs
```

The importer only accepts files under
`reports/dynamic_skip_focus/partitions/` with partition artifact suffixes. It
skips matching existing files and fails on conflicting file sizes unless
`--overwrite` is supplied.

## Rules

- Do not run the same assignment on two workers unless the coordinator has
  already imported one result and the second worker uses skip-existing behavior.
- Transfer compressed artifacts (`.csv.gz`) plus matching partition manifests.
- Transfer the worker counts CSV with the worker plan before running; the plan
  references that local counts file.
- Treat `partition_run_status.csv` as local worker telemetry, not as the final
  source of truth.
- Coordinator regenerates reports after imports and is the only machine that
  commits or pushes.
