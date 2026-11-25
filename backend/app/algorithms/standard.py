from math import inf
from time import perf_counter_ns

from app.algorithms.common import STANDARD_VERSION, build_result, validate_algorithm_nodes
from app.models.route import RouteResult
from app.services.graph_service import InMemoryGraph


def dijkstra_standard(
    graph: InMemoryGraph,
    source_id: str,
    destination_id: str,
) -> RouteResult:
    validate_algorithm_nodes(graph, source_id, destination_id)
    started_at = perf_counter_ns()

    distances = {node_id: inf for node_id in graph.node_ids}
    previous: dict[str, str] = {}
    unvisited = set(graph.node_ids)
    distances[source_id] = 0.0
    visited_nodes = 0
    processed_edges = 0

    while unvisited:
        current = min(unvisited, key=lambda node_id: (distances[node_id], node_id))
        if distances[current] == inf:
            break

        unvisited.remove(current)
        visited_nodes += 1

        for neighbor, weight in graph.adjacency[current]:
            processed_edges += 1
            candidate_distance = distances[current] + weight
            if candidate_distance < distances[neighbor]:
                distances[neighbor] = candidate_distance
                previous[neighbor] = current

    elapsed_ns = perf_counter_ns() - started_at
    return build_result(
        graph=graph,
        algorithm="standard",
        algorithm_version=STANDARD_VERSION,
        source_id=source_id,
        destination_id=destination_id,
        distances=distances,
        previous=previous,
        execution_time_ns=elapsed_ns,
        visited_nodes=visited_nodes,
        processed_edges=processed_edges,
    )
