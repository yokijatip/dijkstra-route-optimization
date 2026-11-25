from fastapi import APIRouter, HTTPException

from app.models.graph import DatasetDetail, DatasetSummary
from app.services.dataset_service import get_dataset_detail, get_dataset_summaries


router = APIRouter(prefix="/api/datasets", tags=["datasets"])


@router.get("", response_model=list[DatasetSummary])
def list_datasets() -> list[DatasetSummary]:
    try:
        return get_dataset_summaries()
    except ValueError as error:
        raise HTTPException(status_code=500, detail=str(error)) from error


@router.get("/{dataset_id}", response_model=DatasetDetail)
def dataset_detail(dataset_id: str) -> DatasetDetail:
    try:
        return get_dataset_detail(dataset_id)
    except FileNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    except ValueError as error:
        raise HTTPException(status_code=500, detail=str(error)) from error
