from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

import app.repositories.genre as genre_repository
import app.models.genre as genre_models

async def get_genres(db: AsyncSession) -> List[genre_models.Genre]:
    """Service pour récupérer une liste de genres."""
    return await genre_repository.get_genres(db)