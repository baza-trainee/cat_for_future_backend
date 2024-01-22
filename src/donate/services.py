from datetime import datetime, timedelta
import hashlib
import hmac
from uuid import uuid4
from urllib.parse import urlparse

import httpx
from fastapi.requests import Request
from fastapi import HTTPException, status

from src.config import settings
from src.donate.schemas import DonateRequestSchema
from src.exceptions import SERVER_ERROR


async def get_payment_url(request: Request, schema: DonateRequestSchema):
    try:
        amount = round(schema.amount, 2)
        payment_body = {
            "merchantAccount": settings.MERCHANT_ACCOUNT,
            "merchantDomainName": urlparse(settings.SITE_URL).netloc,
            "orderReference": str(uuid4()),
            "orderDate": str(int((datetime.utcnow() - timedelta(days=1)).timestamp())),
            "amount": str(amount),
            "currency": "UAH",
            "productName": "Cat for future support",
            "productCount": "1",
            "productPrice": str(amount),
        }
        signature_data = ";".join(payment_body.values())
        merchant_signature = hmac.new(
            settings.MERCHANT_SECRET.encode("utf-8"),
            signature_data.encode("utf-8"),
            hashlib.md5,
        ).hexdigest()

        payment_body.update(
            {
                "language": "UA",
                "returnUrl": request.url_for("approve"),
                "merchantSignature": merchant_signature,
            }
        )
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url="https://secure.wayforpay.com/pay", data=payment_body
            )

        return str(response.next_request.url)

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=SERVER_ERROR
        )
