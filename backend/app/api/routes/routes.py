from fastapi import APIRouter, HTTPException

from app.models.route import CompareResponse, RouteRequest, RouteResult
from app.services.route_service import compare_routes, run_route


router = APIRouter(prefix="/api/routes", tags=["routes"])


def _handle_route_error(error: Exception) -> HTTPException:
    if isinstance(error, FileNotFoundError):
        return HTTPException(status_code=404, detail=str(error))
    return HTTPException(status_code=422, detail=str(error))


@router.post("/standard", response_model=RouteResult)
def run_standard(request: RouteRequest) -> RouteResult:
    try:
        return run_route(request, "standard")
    except (FileNotFoundError, ValueError) as error:
        raise _handle_route_error(error) from error


@router.post("/optimized", response_model=RouteResult)
def run_optimized(request: RouteRequest) -> RouteResult:
    try:
        return run_route(request, "optimized")
    except (FileNotFoundError, ValueError) as error:
        raise _handle_route_error(error) from error


@router.post("/compare", response_model=CompareResponse)
def run_compare(request: RouteRequest) -> CompareResponse:
    try:
        return compare_routes(request)
    except (FileNotFoundError, ValueError) as error:
        raise _handle_route_error(error) from error
