from fastapi import Depends, status, APIRouter
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from typing import Annotated

from pydantic import UUID4
from typing import List

from src.schema import publication_schema
from src.service.publication_service import PublicationService
from src.dependencies import dependencies

router = APIRouter(
    prefix="/api",
    tags=['Publications']
)

token_auth_scheme = HTTPBearer()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=str)
async def create_publication(
        request: publication_schema.Request = Depends(),
        token: HTTPAuthorizationCredentials = Depends(token_auth_scheme),
        publication_service: PublicationService = Depends(PublicationService)
):
    """
    Create a new publication
    """

    return publication_service.create(
        request,
        token,
        await publication_service.upload_image(request.images))


@router.get("/{publication_id}", status_code=status.HTTP_200_OK, response_model=publication_schema.GetResponse)
def get_publication(
        publication_id: UUID4,
        publication_service: PublicationService = Depends(PublicationService)
):
    """
    Get a publication by id
    """
    return publication_service.get(publication_id)


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[publication_schema.GetResponse])
def get_publications(
        pagination: Annotated[publication_schema.Pagination, Depends(dependencies.pagination_params)],
        publication_service: PublicationService = Depends(PublicationService),
        _filter: publication_schema.Filter = Depends()
):
    """
    Get publications
    """
    return None

@router.post("/suggestions/{suggestion}", status_code=status.HTTP_200_OK, response_model=publication_schema.Suggestions)
def get_suggestions(
        suggestion: str,
        publication_service: PublicationService = Depends(PublicationService),

):
    """
    Get suggestions for publications
    """
    return publication_service.get_suggestions(suggestion)


@router.post("/search", status_code=status.HTTP_200_OK)
def search(
        search_filter: publication_schema.SearchFilter,
        pagination: Annotated[publication_schema.Pagination, Depends(dependencies.pagination_params)],
        publication_service: PublicationService = Depends(PublicationService),

):
    """
    Search publications
    """
    return publication_service.search(pagination, search_filter)
