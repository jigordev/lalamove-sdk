import httpx
from datetime import datetime
from lalamove.client import APIClient
from pydantic import BaseModel


class DriverCoord(BaseModel):
    lat: str
    lng: str
    updated_at: datetime


class DriverResponseData(BaseModel):
    driver_id: str
    name: str
    phone: str
    plate_number: str
    photo: str
    coordinates: DriverCoord


class DriverResponse(BaseModel):
    data: DriverResponseData


class Driver:
    def __init__(self, client: APIClient):
        self.client = client

    def get_details(self, order_id: str, driver_id: str) -> DriverResponse:
        response = self.client.make_request(
            "GET", f"orders/{order_id}/drivers/{driver_id}"
        )
        return DriverResponse.modal_validate({"data": response.json()})

    def change(self, order_id: str, driver_id: str) -> DriverResponse:
        response = self.client.make_request(
            "DELETE", f"orders/{order_id}/drivers/{driver_id}"
        )

        try:
            response.raise_for_status()
            return True
        except httpx.HttpStatusError:
            return False
