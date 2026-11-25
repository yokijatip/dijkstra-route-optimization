import csv
from io import StringIO

from fastapi import APIRouter, HTTPException, Response, status
from fastapi.responses import StreamingResponse

from app.models.benchmark import (
    BenchmarkRequest,
    BenchmarkResponse,
    ExperimentHistoryItem,
)
from app.services.benchmark_service import (
    get_benchmark,
    get_experiment_history,
    run_benchmark,
)


router = APIRouter(tags=["benchmarks"])


@router.post(
    "/api/benchmarks",
    response_model=BenchmarkResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_benchmark(request: BenchmarkRequest) -> BenchmarkResponse:
    try:
        return run_benchmark(request)
    except FileNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error


@router.get("/api/benchmarks/{experiment_id}", response_model=BenchmarkResponse)
def benchmark_detail(experiment_id: str) -> BenchmarkResponse:
    try:
        return get_benchmark(experiment_id)
    except FileNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@router.get("/api/experiments", response_model=list[ExperimentHistoryItem])
def experiment_history() -> list[ExperimentHistoryItem]:
    return get_experiment_history()


@router.get("/api/experiments/{experiment_id}", response_model=BenchmarkResponse)
def experiment_detail(experiment_id: str) -> BenchmarkResponse:
    return benchmark_detail(experiment_id)


@router.get("/api/experiments/{experiment_id}/export.csv")
def export_experiment_csv(experiment_id: str) -> Response:
    try:
        benchmark = get_benchmark(experiment_id)
    except FileNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error

    fields = [
        "id",
        "experimentId",
        "datasetId",
        "datasetVersion",
        "sourceId",
        "destinationId",
        "algorithm",
        "algorithmVersion",
        "executionTimeNs",
        "executionTimeMs",
        "visitedNodes",
        "processedEdges",
        "totalCost",
        "path",
        "pathLength",
        "status",
        "createdAt",
    ]
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=fields)
    writer.writeheader()
    for run in benchmark.runs:
        row = run.model_dump(by_alias=True)
        row["path"] = "->".join(run.path)
        writer.writerow(row)

    filename = f"{experiment_id}.csv"
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
