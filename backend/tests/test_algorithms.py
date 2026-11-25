import pytest
from pydantic import ValidationError

from app.algorithms.optimized import dijkstra_optimized
from app.algorithms.standard import dijkstra_standard
from app.models.graph import GraphDataset
from app.services.graph_service import build_in_memory_graph
from app.services.dataset_service import get_graph


def graph_from_payload(payload: dict):
    return build_in_memory_graph(GraphDataset.model_validate(payload))


def test_standard_and_optimized_return_same_shortest_cost():
    graph = get_graph("small-demo")

    standard = dijkstra_standard(graph, "soreang", "baleendah")
    optimized = dijkstra_optimized(graph, "soreang", "baleendah")

    assert standard.status == "success"
    assert optimized.status == "success"
    assert standard.total_cost == pytest.approx(9.2)
    assert optimized.total_cost == pytest.approx(9.2)
    assert standard.total_cost == pytest.approx(optimized.total_cost)
    assert standard.path_length == len(standard.path) - 1
    assert optimized.path_length == len(optimized.path) - 1


def test_source_equal_destination_has_zero_cost():
    graph = get_graph("small-demo")

    result = dijkstra_optimized(graph, "soreang", "soreang")

    assert result.status == "success"
    assert result.path == ["soreang"]
    assert result.total_cost == 0
    assert result.path_length == 0


def test_unreachable_destination_is_reported():
    graph = graph_from_payload(
        {
            "id": "disconnected",
            "name": "Disconnected",
            "version": "1.0.0",
            "nodes": [
                {"id": "a", "name": "A"},
                {"id": "b", "name": "B"},
            ],
            "edges": [],
        }
    )

    result = dijkstra_standard(graph, "a", "b")

    assert result.status == "unreachable"
    assert result.path == []
    assert result.total_cost is None


def test_negative_weight_is_rejected():
    with pytest.raises(ValidationError):
        GraphDataset.model_validate(
            {
                "id": "invalid",
                "name": "Invalid",
                "version": "1.0.0",
                "nodes": [
                    {"id": "a", "name": "A"},
                    {"id": "b", "name": "B"},
                ],
                "edges": [
                    {"from": "a", "to": "b", "weight": -1},
                ],
            }
        )
