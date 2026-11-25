from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from app.models.route import RouteStatus


class BenchmarkPair(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    source_id: str = Field(alias="sourceId", min_length=1)
    destination_id: str = Field(alias="destinationId", min_length=1)


class BenchmarkRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    dataset_id: str = Field(default="small-demo", alias="datasetId", min_length=1)
    test_case_count: int = Field(default=10, alias="testCaseCount", ge=1, le=1000)
    pair_mode: Literal["preset", "random"] = Field(default="random", alias="pairMode")
    pairs: list[BenchmarkPair] | None = Field(default=None, max_length=1000)
    warmup_runs: int = Field(default=1, alias="warmupRuns", ge=0, le=10)
    repeat_count: int = Field(default=3, alias="repeatCount", ge=1, le=50)
    random_seed: int | None = Field(default=42, alias="randomSeed")
    tolerance: float = Field(default=1e-9, gt=0, le=1)


class BenchmarkRun(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str
    experiment_id: str = Field(alias="experimentId")
    dataset_id: str = Field(alias="datasetId")
    dataset_version: str = Field(alias="datasetVersion")
    source_id: str = Field(alias="sourceId")
    destination_id: str = Field(alias="destinationId")
    algorithm: Literal["standard", "optimized"]
    algorithm_version: str = Field(alias="algorithmVersion")
    execution_time_ns: int = Field(alias="executionTimeNs", ge=0)
    execution_time_ms: float = Field(alias="executionTimeMs", ge=0)
    visited_nodes: int = Field(alias="visitedNodes", ge=0)
    processed_edges: int = Field(alias="processedEdges", ge=0)
    total_cost: float | None = Field(alias="totalCost", default=None)
    path: list[str]
    path_length: int = Field(alias="pathLength", ge=0)
    status: RouteStatus
    created_at: datetime = Field(alias="createdAt")


class AggregateMetrics(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    run_count: int = Field(alias="runCount")
    success_count: int = Field(alias="successCount")
    unreachable_count: int = Field(alias="unreachableCount")
    mean_execution_time_ns: float = Field(alias="meanExecutionTimeNs")
    median_execution_time_ns: float = Field(alias="medianExecutionTimeNs")
    minimum_execution_time_ns: int = Field(alias="minimumExecutionTimeNs")
    maximum_execution_time_ns: int = Field(alias="maximumExecutionTimeNs")
    standard_deviation_execution_time_ns: float = Field(alias="standardDeviationExecutionTimeNs")
    mean_execution_time_ms: float = Field(alias="meanExecutionTimeMs")
    mean_visited_nodes: float = Field(alias="meanVisitedNodes")
    mean_processed_edges: float = Field(alias="meanProcessedEdges")
    mean_path_length: float = Field(alias="meanPathLength")


class BenchmarkSummary(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    experiment_id: str = Field(alias="experimentId")
    dataset_id: str = Field(alias="datasetId")
    dataset_version: str = Field(alias="datasetVersion")
    test_case_count: int = Field(alias="testCaseCount")
    repeat_count: int = Field(alias="repeatCount")
    warmup_runs: int = Field(alias="warmupRuns")
    pair_mode: str = Field(alias="pairMode")
    random_seed: int | None = Field(alias="randomSeed")
    correctness_mismatch_count: int = Field(alias="correctnessMismatchCount")
    standard: AggregateMetrics
    optimized: AggregateMetrics
    improvement: dict[str, float]
    created_at: datetime = Field(alias="createdAt")


class BenchmarkResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    summary: BenchmarkSummary
    runs: list[BenchmarkRun]


class ExperimentHistoryItem(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    experiment_id: str = Field(alias="experimentId")
    dataset_id: str = Field(alias="datasetId")
    dataset_version: str = Field(alias="datasetVersion")
    test_case_count: int = Field(alias="testCaseCount")
    repeat_count: int = Field(alias="repeatCount")
    correctness_mismatch_count: int = Field(alias="correctnessMismatchCount")
    created_at: datetime = Field(alias="createdAt")
