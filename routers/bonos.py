from fastapi import APIRouter
from services.rava_scraper import get_bonos

router = APIRouter()

@router.get("/bonos")
def obtener_bonos():
    return get_bonos()