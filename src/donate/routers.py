from fastapi import APIRouter, Request, status
from fastapi.responses import RedirectResponse

from .schemas import DonateRequestSchema, DonateResponseSchema
from .services import get_payment_url
from src.config import settings

donate_router = APIRouter(prefix="/donate", tags=["Donate"])


@donate_router.post("", response_model=DonateResponseSchema)
async def donate(request: Request, schema: DonateRequestSchema):
    payment_url = await get_payment_url(request=request, schema=schema)
    return {"payment_url": payment_url}


@donate_router.get("/approve", include_in_schema=False)
def approve() -> RedirectResponse:
    return RedirectResponse(
        f"{settings.SITE_URL}/?payment=success",
        status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    )
