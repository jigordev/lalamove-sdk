from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from lalamove.client import APIClient
from lalamove.constants import Languages


class QuotationCoord(BaseModel):
    lat: str
    lng: str


class QuotationStop(BaseModel):
    stop_id: Optional[str]
    coordinates: QuotationCoord
    address: str


class QuotationItem(BaseModel):
    quantity: str
    weight: str
    categories: List[str]
    handling_instructions: List[str]


class QuotationData(BaseModel):
    service_type: str
    stops: List[QuotationStop]
    language: Languages
    schedule_at: Optional[datetime]
    special_requests: Optional[List[str]]
    is_route_optimized: Optional[bool] = False
    item: Optional[QuotationItem]


class QuotationBody(BaseModel):
    data: QuotationData


class QuotationPriceBreakdown(BaseModel):
    base: str
    special_requests: str
    vat: str
    total_before_optimization: str
    total_exclude_priority_fee: str
    total: str
    currency: str


class QuotationResponseData(BaseModel):
    quotation_id: str
    schedule_at: Optional[datetime]
    expires_at: datetime
    service_type: str
    special_requests: Optional[List[str]]
    language: str
    stops: List[QuotationStop]
    is_route_optimized: bool
    price_breakdown: QuotationPriceBreakdown
    item: Optional[QuotationItem]


class QuotationResponse(BaseModel):
    data: QuotationResponseData


class Quotation:
    def __init__(self, client: APIClient):
        self.client = client

    def create(self, data: QuotationData) -> QuotationResponse:
        data = QuotationBody(data=data)
        response = self.client.make_request("POST", "quotations", data.model_dump())
        return QuotationResponse.model_validate({"data": response})

    def get_details(self, quotation_id: str) -> QuotationResponse:
        response = self.client.make_request("GET", f"quotations/{quotation_id}")
        return QuotationResponse.model_validate({"data": response})
