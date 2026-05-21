from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime


class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    category: Optional[str] = None
    default_quantity: float = 1.0
    quantity_unit: str = "each"  # per_day, per_trip, each
    tags: Optional[str] = None  # comma-separated
    notes: Optional[str] = None


class Activity(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    # store items as JSON string: list of {item_id:int, multiplier:float}
    items_json: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Trip(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    duration_days: int = 1
    travellers: int = 1
    activity_ids_json: Optional[str] = None
    items_json: Optional[str] = None
    reminders_json: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
