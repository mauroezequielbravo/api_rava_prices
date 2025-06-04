from fastapi import APIRouter
from services.rava_scraper import get_cedear

router = APIRouter()

@router.get("/cedears")
def obtener_cedears():
    return get_cedear()