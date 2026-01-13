from fastapi import Request, status
from fastapi.responses import JSONResponse
from app.core.exceptions import NotFoundBLLException, ValidationBLLException, DALException, BLLException

async def not_found_bll_exception_handler(request: Request, exc: NotFoundBLLException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)},
    )

async def validation_bll_exception_handler(request: Request, exc: ValidationBLLException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)},
    )

async def bll_exception_handler(request: Request, exc: BLLException):
    """Gestionnaire pour les autres erreurs métier non spécifiques."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)},
    )

async def dal_exception_handler(request: Request, exc: DALException):
    # En production, on devrait logger l'exception originale: exc.original_exception
    print(f"DAL Error: {exc.original_exception}") # Pour le debug
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Une erreur interne est survenue au niveau de la base de données."},
    )

# Note : cela évite de devoir gérer les exceptions de type DAL et BLL dans les routeurs FastAPI directement :
#
# @router.get("/movies/{movie_id}", response_model=movie_schemas.Movie)
# async def read_movie(movie_id: int, db: AsyncSession = Depends(get_db)):
#    """Récupère les détails d'un film spécifique par son ID."""
#    try:
#        return await movie_service.get_movie_by_id(db=db, movie_id=movie_id)
#    except NotFoundError as e:
#       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
#    except DALException as e:
#       # Logguer l'erreur originale (e.original_exception) serait une bonne pratique ici
#       raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erreur interne du serveur.")
