from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


AlgorithmName = Literal["standard", "optimized"]
RouteStatus = Literal["success", "unreachable", "error"]


class RouteRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    dataset_id: str = Field(default="small-demo", alias="datasetId", min_length=1)
    source_id: str = Field(alias="sourceId", min_length=1)
    destination_id: str = Field(alias="destinationId", min_length=1)
    tolerance: float = Field(default=1e-9, gt=0, le=1)


class RouteResult(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    algorithm: AlgorithmName
    algorithm_version: str = Field(alias="algorithmVersion")
    dataset_id: str = Field(alias="datasetId")
    dataset_version: str = Field(alias="datasetVersion")
    source_id: str = Field(alias="sourceId")
    destination_id: str = Field(alias="destinationId")
    status: RouteStatus
    path: list[str]
    path_length: int = Field(alias="pathLength", ge=0)
    total_cost: float | None = Field(alias="totalCost", default=None)
    execution_time_ns: int = Field(alias="executionTimeNs", ge=0)
    execution_time_ms: float = Field(alias="executionTimeMs", ge=0)
    visited_nodes: int = Field(alias="visitedNodes", ge=0)
    processed_edges: int = Field(alias="processedEdges", ge=0)


class ImprovementMetrics(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    execution_time_pct: float = Field(alias="executionTimePct")
    visited_nodes_pct: float = Field(alias="visitedNodesPct")
    processed_edges_pct: float = Field(alias="processedEdgesPct")


class CompareResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    dataset_id: str = Field(alias="datasetId")
    dataset_version: str = Field(alias="datasetVersion")
    source_id: str = Field(alias="sourceId")
    destination_id: str = Field(alias="destinationId")
    standard: RouteResult
    optimized: RouteResult
    correctness_match: bool = Field(alias="correctnessMatch")
    tolerance: float
    improvement: ImprovementMetrics
