from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class PriceInput(BaseModel):
    gram_18k: float = Field(ge=0)
    half_coin: float = Field(ge=0)
    quarter_coin: float = Field(ge=0)
    bahar_coin: float = Field(ge=0)


class PriceOutput(PriceInput):
    id: int


class HoldingInput(BaseModel):
    asset_type: str
    quantity: float = Field(ge=0)


class HoldingOutput(HoldingInput):
    id: int


class PortfolioSummary(BaseModel):
    total_irt: float
    by_asset: dict[str, float]
