from math import isclose

from app.algorithms.optimized import dijkstra_optimized
from app.algorithms.standard import dijkstra_standard
from app.models.route import CompareResponse, ImprovementMetrics, RouteRequest, RouteResult
from app.services.dataset_service import get_graph


def run_route(request: RouteRequest, algorithm: str) -> RouteResult:
    graph = get_graph(request.dataset_id)
    if algorithm == "standard":
        return dijkstra_standard(graph, request.source_id, request.destination_id)
    return dijkstra_optimized(graph, request.source_id, request.destination_id)


def _improvement(baseline: float, optimized: float) -> float:
    if baseline == 0:
        return 0.0
    return (baseline - optimized) / baseline * 100


def compare_routes(request: RouteRequest) -> CompareResponse:
    standard = run_route(request, "standard")
    optimized = run_route(request, "optimized")

    if standard.total_cost is None or optimized.total_cost is None:
        correctness_match = standard.status == optimized.status
    else:
        correctness_match = isclose(
            standard.total_cost,
            optimized.total_cost,
            rel_tol=0,
            abs_tol=request.tolerance,
        )

    return CompareResponse(
        datasetId=request.dataset_id,
        datasetVersion=standard.dataset_version,
        sourceId=request.source_id,
        destinationId=request.destination_id,
        standard=standard,
        optimized=optimized,
        correctnessMatch=correctness_match,
        tolerance=request.tolerance,
        improvement=ImprovementMetrics(
            executionTimePct=_improvement(
                standard.execution_time_ns,
                optimized.execution_time_ns,
            ),
            visitedNodesPct=_improvement(
                standard.visited_nodes,
                optimized.visited_nodes,
            ),
            processedEdgesPct=_improvement(
                standard.processed_edges,
                optimized.processed_edges,
            ),
        ),
    )
