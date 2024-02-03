from fastapi import Depends, status, APIRouter, File, UploadFile
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.schema import publication_schema
from app.service.publication_service import PublicationService


router = APIRouter(
    prefix="/api",
    tags=['Publications']
)

token_auth_scheme = HTTPBearer()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_publication(
        request: publication_schema.Request = Depends(),
        token: HTTPAuthorizationCredentials = Depends(token_auth_scheme),
        publication_service: PublicationService = Depends(PublicationService)
):
    """
    Create a new publication
    """
    create_response = publication_service.create(
        request,
        token,
        await publication_service.upload_image(request.images))

    return create_response


