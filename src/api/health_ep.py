from fastapi import status, APIRouter

router = APIRouter(
    prefix="/api",
    tags=['Health Check']
)


@router.get("/sentry-debug", status_code=status.HTTP_200_OK)
async def trigger_error():
    """
    Verify the Sentry error tracking.
    """
    division_by_zero = 1 / 0
