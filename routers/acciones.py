from fastapi import APIRouter
from services.rava_scraper import get_acciones

router = APIRouter()

@router.get("/acciones")
def obtener_acciones():
    return get_acciones()