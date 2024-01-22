from pydantic import AnyHttpUrl, BaseModel, confloat


class DonateRequestSchema(BaseModel):
    amount: confloat(ge=1)


class DonateResponseSchema(BaseModel):
    payment_url: AnyHttpUrl
