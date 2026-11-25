from dataclasses import dataclass
from typing import Mapping

from app.models.graph import GraphDataset


@dataclass(frozen=True, slots=True)
class InMemoryGraph:
    dataset: GraphDataset
    adjacency: Mapping[str, tuple[tuple[str, float], ...]]

    @property
    def node_ids(self) -> tuple[str, ...]:
        return tuple(self.adjacency.keys())


def build_in_memory_graph(dataset: GraphDataset) -> InMemoryGraph:
    adjacency: dict[str, list[tuple[str, float]]] = {
        node.id: [] for node in dataset.nodes
    }

    for edge in dataset.edges:
        adjacency[edge.from_].append((edge.to, float(edge.weight)))
        if edge.bidirectional and edge.from_ != edge.to:
            adjacency[edge.to].append((edge.from_, float(edge.weight)))

    return InMemoryGraph(
        dataset=dataset,
        adjacency={node_id: tuple(neighbors) for node_id, neighbors in adjacency.items()},
    )
