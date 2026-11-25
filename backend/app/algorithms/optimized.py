import heapq
from math import inf
from time import perf_counter_ns

from app.algorithms.common import OPTIMIZED_VERSION, build_result, validate_algorithm_nodes
from app.models.route import RouteResult
from app.services.graph_service import InMemoryGraph


def dijkstra_optimized(
    graph: InMemoryGraph,
    source_id: str,
    destination_id: str,
) -> RouteResult:
    validate_algorithm_nodes(graph, source_id, destination_id)
    started_at = perf_counter_ns()

    distances = {node_id: inf for node_id in graph.node_ids}
    previous: dict[str, str] = {}
    distances[source_id] = 0.0
    frontier: list[tuple[float, str]] = [(0.0, source_id)]
    settled: set[str] = set()
    visited_nodes = 0
    processed_edges = 0

    while frontier:
        current_distance, current = heapq.heappop(frontier)
        if current in settled or current_distance > distances[current]:
            continue

        settled.add(current)
        visited_nodes += 1

        if current == destination_id:
            break

        for neighbor, weight in graph.adjacency[current]:
            processed_edges += 1
            candidate_distance = current_distance + weight
            if candidate_distance < distances[neighbor]:
                distances[neighbor] = candidate_distance
                previous[neighbor] = current
                heapq.heappush(frontier, (candidate_distance, neighbor))

    elapsed_ns = perf_counter_ns() - started_at
    return build_result(
        graph=graph,
        algorithm="optimized",
        algorithm_version=OPTIMIZED_VERSION,
        source_id=source_id,
        destination_id=destination_id,
        distances=distances,
        previous=previous,
        execution_time_ns=elapsed_ns,
        visited_nodes=visited_nodes,
        processed_edges=processed_edges,
    )
