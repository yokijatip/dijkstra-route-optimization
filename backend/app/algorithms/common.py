from collections.abc import Mapping, Sequence
from math import isfinite

from app.models.route import RouteResult
from app.services.graph_service import InMemoryGraph


STANDARD_VERSION = "standard-v1-linear-scan"
OPTIMIZED_VERSION = "optimized-v1-min-heap-early-termination"

Adjacency = Mapping[str, Sequence[tuple[str, float]]]


def validate_algorithm_nodes(graph: InMemoryGraph, source_id: str, destination_id: str) -> None:
    if source_id not in graph.adjacency:
        raise ValueError(f"Source node tidak ditemukan: {source_id}")
    if destination_id not in graph.adjacency:
        raise ValueError(f"Destination node tidak ditemukan: {destination_id}")


def reconstruct_path(
    previous: Mapping[str, str],
    source_id: str,
    destination_id: str,
) -> list[str]:
    path = [destination_id]
    current = destination_id
    while current != source_id:
        current = previous.get(current, "")
        if not current:
            return []
        path.append(current)
    path.reverse()
    return path


def build_result(
    *,
    graph: InMemoryGraph,
    algorithm: str,
    algorithm_version: str,
    source_id: str,
    destination_id: str,
    distances: Mapping[str, float],
    previous: Mapping[str, str],
    execution_time_ns: int,
    visited_nodes: int,
    processed_edges: int,
) -> RouteResult:
    total_cost = distances.get(destination_id, float("inf"))
    reachable = isfinite(total_cost)
    path = reconstruct_path(previous, source_id, destination_id) if reachable else []

    return RouteResult(
        algorithm=algorithm,
        algorithmVersion=algorithm_version,
        datasetId=graph.dataset.id,
        datasetVersion=graph.dataset.version,
        sourceId=source_id,
        destinationId=destination_id,
        status="success" if reachable else "unreachable",
        path=path,
        pathLength=max(len(path) - 1, 0),
        totalCost=total_cost if reachable else None,
        executionTimeNs=execution_time_ns,
        executionTimeMs=execution_time_ns / 1_000_000,
        visitedNodes=visited_nodes,
        processedEdges=processed_edges,
    )
