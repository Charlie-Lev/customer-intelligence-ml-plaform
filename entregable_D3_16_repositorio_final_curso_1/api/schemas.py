from pydantic import BaseModel, Field

class CustomerInput(BaseModel):
    customer_id: str
    age: float = Field(gt=0, le=120)
    tenure_months: int = Field(ge=0)
    monthly_fee: float = Field(ge=0)
    total_spent: float = Field(ge=0)
    support_calls: int = Field(ge=0)
    complaints: int = Field(ge=0)
    last_payment_delay: int = Field(ge=0)
    digital_usage_score: float
    marketing_score: float
    preferred_contact_hour: int = Field(ge=0, le=23)
    gender: str
    region: str
    customer_segment: str
    contract_type: str
    internet_service: str
    tv_service: str
    streaming_service: str
    payment_method: str

class PredictionResponse(BaseModel):
    customer_id: str | None = None
    churn_probability: float
    churn_prediction: int
