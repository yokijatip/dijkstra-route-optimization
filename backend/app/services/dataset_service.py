import json
import re
from functools import lru_cache
from pathlib import Path

from app.models.graph import DatasetDetail, DatasetSummary, GraphDataset
from app.services.graph_service import InMemoryGraph, build_in_memory_graph


DATASET_DIRECTORY = Path(__file__).resolve().parents[1] / "data" / "datasets"
DATASET_ID_PATTERN = re.compile(r"^[A-Za-z0-9_-]+$")


def _dataset_path(dataset_id: str) -> Path:
    if not DATASET_ID_PATTERN.fullmatch(dataset_id):
        raise FileNotFoundError(f"Dataset tidak ditemukan: {dataset_id}")
    return DATASET_DIRECTORY / f"{dataset_id}.json"


@lru_cache(maxsize=16)
def get_graph(dataset_id: str) -> InMemoryGraph:
    path = _dataset_path(dataset_id)
    if not path.is_file():
        raise FileNotFoundError(f"Dataset tidak ditemukan: {dataset_id}")

    with path.open("r", encoding="utf-8") as dataset_file:
        payload = json.load(dataset_file)

    dataset = GraphDataset.model_validate(payload)
    return build_in_memory_graph(dataset)


def get_dataset_summaries() -> list[DatasetSummary]:
    summaries: list[DatasetSummary] = []
    for path in sorted(DATASET_DIRECTORY.glob("*.json")):
        graph = get_graph(path.stem)
        dataset = graph.dataset
        summaries.append(
            DatasetSummary(
                id=dataset.id,
                name=dataset.name,
                version=dataset.version,
                description=dataset.description,
                source=dataset.source,
                region=dataset.region,
                networkType=dataset.network_type,
                weightUnit=dataset.weight_unit,
                nodeCount=len(dataset.nodes),
                edgeCount=len(dataset.edges),
                validationStatus="valid",
            )
        )
    return summaries


def get_dataset_detail(dataset_id: str) -> DatasetDetail:
    dataset = get_graph(dataset_id).dataset
    return DatasetDetail(
        **dataset.model_dump(),
        nodeCount=len(dataset.nodes),
        edgeCount=len(dataset.edges),
        validationStatus="valid",
    )
