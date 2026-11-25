import random
import statistics
from datetime import datetime, timezone
from itertools import count
from uuid import uuid4

from app.algorithms.optimized import dijkstra_optimized
from app.algorithms.standard import dijkstra_standard
from app.models.benchmark import (
    AggregateMetrics,
    BenchmarkPair,
    BenchmarkRequest,
    BenchmarkResponse,
    BenchmarkRun,
    BenchmarkSummary,
    ExperimentHistoryItem,
)
from app.models.route import RouteResult
from app.services.dataset_service import get_graph
from app.services.firebase_service import (
    get_benchmark as get_firestore_benchmark,
    get_experiment_history as get_firestore_history,
    save_benchmark as save_benchmark_to_firestore,
)
from app.services.graph_service import InMemoryGraph


_EXPERIMENTS: dict[str, BenchmarkResponse] = {}


def _build_random_pairs(graph: InMemoryGraph, request: BenchmarkRequest) -> list[BenchmarkPair]:
    node_ids = list(graph.node_ids)
    if len(node_ids) < 2:
        raise ValueError("Benchmark membutuhkan minimal dua node")

    maximum_pairs = len(node_ids) * (len(node_ids) - 1)
    if request.test_case_count > maximum_pairs:
        raise ValueError(
            f"testCaseCount maksimal untuk dataset ini adalah {maximum_pairs}"
        )

    generator = random.Random(request.random_seed)
    selected: set[tuple[str, str]] = set()
    pairs: list[BenchmarkPair] = []
    while len(pairs) < request.test_case_count:
        source_id, destination_id = generator.sample(node_ids, 2)
        pair = (source_id, destination_id)
        if pair in selected:
            continue
        selected.add(pair)
        pairs.append(
            BenchmarkPair(sourceId=source_id, destinationId=destination_id)
        )
    return pairs


def _build_preset_pairs(graph: InMemoryGraph, request: BenchmarkRequest) -> list[BenchmarkPair]:
    if request.pairs is not None:
        if len(request.pairs) < request.test_case_count:
            raise ValueError("Jumlah pairs harus memenuhi testCaseCount")
        pairs = request.pairs[: request.test_case_count]
    else:
        node_ids = list(graph.node_ids)
        if len(node_ids) < 2:
            raise ValueError("Benchmark membutuhkan minimal dua node")
        pairs = [
            BenchmarkPair(
                sourceId=node_ids[index % len(node_ids)],
                destinationId=node_ids[(index + 1) % len(node_ids)],
            )
            for index in range(request.test_case_count)
        ]

    for pair in pairs:
        if pair.source_id == pair.destination_id:
            raise ValueError("Source dan destination pada benchmark harus berbeda")
        if pair.source_id not in graph.adjacency:
            raise ValueError(f"Source node tidak ditemukan: {pair.source_id}")
        if pair.destination_id not in graph.adjacency:
            raise ValueError(f"Destination node tidak ditemukan: {pair.destination_id}")
    return pairs


def build_test_cases(graph: InMemoryGraph, request: BenchmarkRequest) -> list[BenchmarkPair]:
    if request.pair_mode == "preset":
        return _build_preset_pairs(graph, request)
    return _build_random_pairs(graph, request)


def _costs_match(standard: RouteResult, optimized: RouteResult, tolerance: float) -> bool:
    if standard.status != optimized.status:
        return False
    if standard.total_cost is None or optimized.total_cost is None:
        return standard.total_cost is None and optimized.total_cost is None
    return abs(standard.total_cost - optimized.total_cost) <= tolerance


def _to_benchmark_run(
    result: RouteResult,
    experiment_id: str,
    run_number: int,
) -> BenchmarkRun:
    return BenchmarkRun(
        id=f"{experiment_id}-run-{run_number}",
        experimentId=experiment_id,
        datasetId=result.dataset_id,
        datasetVersion=result.dataset_version,
        sourceId=result.source_id,
        destinationId=result.destination_id,
        algorithm=result.algorithm,
        algorithmVersion=result.algorithm_version,
        executionTimeNs=result.execution_time_ns,
        executionTimeMs=result.execution_time_ms,
        visitedNodes=result.visited_nodes,
        processedEdges=result.processed_edges,
        totalCost=result.total_cost,
        path=result.path,
        pathLength=result.path_length,
        status=result.status,
        createdAt=datetime.now(timezone.utc),
    )


def _aggregate(runs: list[BenchmarkRun]) -> AggregateMetrics:
    if not runs:
        raise ValueError("Tidak ada raw run untuk diagregasi")

    execution_times = [run.execution_time_ns for run in runs]
    return AggregateMetrics(
        runCount=len(runs),
        successCount=sum(run.status == "success" for run in runs),
        unreachableCount=sum(run.status == "unreachable" for run in runs),
        meanExecutionTimeNs=statistics.fmean(execution_times),
        medianExecutionTimeNs=statistics.median(execution_times),
        minimumExecutionTimeNs=min(execution_times),
        maximumExecutionTimeNs=max(execution_times),
        standardDeviationExecutionTimeNs=(
            statistics.pstdev(execution_times) if len(execution_times) > 1 else 0.0
        ),
        meanExecutionTimeMs=statistics.fmean(execution_times) / 1_000_000,
        meanVisitedNodes=statistics.fmean(run.visited_nodes for run in runs),
        meanProcessedEdges=statistics.fmean(run.processed_edges for run in runs),
        meanPathLength=statistics.fmean(run.path_length for run in runs),
    )


def _improvement(baseline: float, optimized: float) -> float:
    if baseline == 0:
        return 0.0
    return (baseline - optimized) / baseline * 100


def run_benchmark(request: BenchmarkRequest) -> BenchmarkResponse:
    graph = get_graph(request.dataset_id)
    pairs = build_test_cases(graph, request)
    experiment_id = uuid4().hex
    runs: list[BenchmarkRun] = []
    mismatch_count = 0
    run_number = count(1)

    for pair in pairs:
        for _ in range(request.warmup_runs):
            dijkstra_standard(graph, pair.source_id, pair.destination_id)
            dijkstra_optimized(graph, pair.source_id, pair.destination_id)

        pair_has_mismatch = False
        for _ in range(request.repeat_count):
            standard = dijkstra_standard(graph, pair.source_id, pair.destination_id)
            optimized = dijkstra_optimized(graph, pair.source_id, pair.destination_id)
            pair_has_mismatch = pair_has_mismatch or not _costs_match(
                standard,
                optimized,
                request.tolerance,
            )
            runs.append(_to_benchmark_run(standard, experiment_id, next(run_number)))
            runs.append(_to_benchmark_run(optimized, experiment_id, next(run_number)))
        mismatch_count += int(pair_has_mismatch)

    standard_runs = [run for run in runs if run.algorithm == "standard"]
    optimized_runs = [run for run in runs if run.algorithm == "optimized"]
    standard_summary = _aggregate(standard_runs)
    optimized_summary = _aggregate(optimized_runs)
    created_at = datetime.now(timezone.utc)

    summary = BenchmarkSummary(
        experimentId=experiment_id,
        datasetId=graph.dataset.id,
        datasetVersion=graph.dataset.version,
        testCaseCount=len(pairs),
        repeatCount=request.repeat_count,
        warmupRuns=request.warmup_runs,
        pairMode=request.pair_mode,
        randomSeed=request.random_seed,
        correctnessMismatchCount=mismatch_count,
        standard=standard_summary,
        optimized=optimized_summary,
        improvement={
            "executionTimePct": _improvement(
                standard_summary.mean_execution_time_ns,
                optimized_summary.mean_execution_time_ns,
            ),
            "visitedNodesPct": _improvement(
                standard_summary.mean_visited_nodes,
                optimized_summary.mean_visited_nodes,
            ),
            "processedEdgesPct": _improvement(
                standard_summary.mean_processed_edges,
                optimized_summary.mean_processed_edges,
            ),
        },
        createdAt=created_at,
    )
    response = BenchmarkResponse(summary=summary, runs=runs)
    _EXPERIMENTS[experiment_id] = response
    save_benchmark_to_firestore(response)
    return response


def get_benchmark(experiment_id: str) -> BenchmarkResponse:
    if experiment_id in _EXPERIMENTS:
        return _EXPERIMENTS[experiment_id]

    persisted = get_firestore_benchmark(experiment_id)
    if persisted is not None:
        _EXPERIMENTS[experiment_id] = persisted
        return persisted

    raise FileNotFoundError(f"Eksperimen tidak ditemukan: {experiment_id}")


def get_experiment_history() -> list[ExperimentHistoryItem]:
    memory_history = [
        ExperimentHistoryItem(
            experimentId=summary.experiment_id,
            datasetId=summary.dataset_id,
            datasetVersion=summary.dataset_version,
            testCaseCount=summary.test_case_count,
            repeatCount=summary.repeat_count,
            correctnessMismatchCount=summary.correctness_mismatch_count,
            createdAt=summary.created_at,
        )
        for response in reversed(list(_EXPERIMENTS.values()))
        for summary in [response.summary]
    ]
    persisted_history = get_firestore_history()
    if persisted_history is None:
        return memory_history

    known_ids = {item.experiment_id for item in persisted_history}
    combined = persisted_history + [
        item for item in memory_history if item.experiment_id not in known_ids
    ]
    return sorted(combined, key=lambda item: item.created_at, reverse=True)
