import random

from scripts.benchmark_performance import random_queries, random_text


def test_random_text_and_queries_use_declared_alphabet() -> None:
    rng = random.Random(1)

    text = random_text(rng, "ab", 20)
    queries = random_queries(rng, "ab", count=3, length=4)

    assert len(text) == 20
    assert set(text) <= {"a", "b"}
    assert len(queries) == 3
    assert all(len(query) == 4 and set(query) <= {"a", "b"} for query in queries)

