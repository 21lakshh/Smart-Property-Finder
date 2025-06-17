from pydantic import BaseModel
from typing import List

class PropertyInput(BaseModel):
    city: str
    min_budget: str | None = None
    max_budget: str | None = None
    property_type: str | None = None # Flat / Individual House
    property_category: str | None = None # Residential / Commercial
    bedrooms: str | None = None
    bathrooms: str | None = None

class Property(BaseModel):
    title: str | None = None
    price: str | None = None
    area: str | None = None
    bedrooms: str | None = None
    bathrooms: str | None = None
    property_type: str | None = None
    property_category: str | None = None
    city: str | None = None
    url: str | None = None
    image_url: str | None = None

