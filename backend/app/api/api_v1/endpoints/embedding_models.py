"""The API module that contains the endpoints for embedding models."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas
from app.api import deps
from app.platform.configs._base import Fields
from app.platform.locator import resources

router = APIRouter()


@router.get("/{short_name}", response_model=schemas.EmbeddingModelWithConfigFields)
async def read_embedding_model(
    *,
    db: AsyncSession = Depends(deps.get_db),
    short_name: str,
    user: schemas.User = Depends(deps.get_user),
) -> schemas.EmbeddingModel:
    """Get embedding model by id.

    Args:
    ----
        db (AsyncSession): The database session.
        short_name (str): The short name of the embedding model.
        user (schemas.User): The current user.

    Returns:
    -------
        schemas.EmbeddingModel: The embedding model object.

    """
    embedding_model = await crud.embedding_model.get_by_short_name(db, short_name)
    if not embedding_model:
        raise HTTPException(status_code=404, detail="Embedding model not found")
    if embedding_model.auth_config_class:
        auth_config_class = resources.get_auth_config(embedding_model.auth_config_class)
        embedding_model.config_fields = Fields.from_config_class(auth_config_class)
    return embedding_model


@router.get("/", response_model=list[schemas.EmbeddingModel])
async def read_embedding_models(
    *,
    db: AsyncSession = Depends(deps.get_db),
    user: schemas.User = Depends(deps.get_user),
) -> list[schemas.EmbeddingModel]:
    """Get all embedding models.

    Args:
    ----
        db (AsyncSession): The database session.
        user (schemas.User): The current user.

    Returns:
    -------
        list[schemas.EmbeddingModel]: The list of embedding models.

    """
    return await crud.embedding_model.get_all(db)
