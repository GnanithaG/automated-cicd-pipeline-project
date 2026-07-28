from enum import StrEnum

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="Risk Scoring Service", version="1.0.0")


class RiskLevel(StrEnum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class RiskRequest(BaseModel):
    customer_id: str = Field(min_length=1)
    amount: float = Field(gt=0)
    international: bool = False
    prior_chargebacks: int = Field(default=0, ge=0)


class RiskResponse(BaseModel):
    customer_id: str
    score: int
    level: RiskLevel
    approved: bool


def calculate_score(request: RiskRequest) -> int:
    score = 10
    if request.amount >= 1000:
        score += 35
    elif request.amount >= 500:
        score += 20
    if request.international:
        score += 20
    score += min(request.prior_chargebacks * 15, 30)
    return min(score, 100)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "UP"}


@app.post("/api/risk", response_model=RiskResponse)
def assess_risk(request: RiskRequest) -> RiskResponse:
    score = calculate_score(request)
    level = RiskLevel.HIGH if score >= 70 else RiskLevel.MEDIUM if score >= 40 else RiskLevel.LOW
    return RiskResponse(
        customer_id=request.customer_id,
        score=score,
        level=level,
        approved=score < 70,
    )
