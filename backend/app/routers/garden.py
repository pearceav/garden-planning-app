import logging

from fastapi import APIRouter, HTTPException

from app.models.requests import GardenPlanRequest
from app.models.responses import GardenPlanResponse
from app.services.claude_service import generate_garden_plan

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/garden", tags=["garden"])


@router.post("/plan", response_model=GardenPlanResponse)
async def create_garden_plan(request: GardenPlanRequest):
    """Generate AI-powered companion planting recommendations."""
    if not request.selected_seeds:
        raise HTTPException(status_code=400, detail="No seeds selected")

    if len(request.selected_seeds) > 200:
        raise HTTPException(status_code=400, detail="Maximum 200 seeds allowed")

    try:
        plan = await generate_garden_plan(request.selected_seeds, request.preferences)
        return plan
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        logger.exception("Unexpected error generating garden plan")
        raise HTTPException(status_code=500, detail="Something went wrong — try again")
