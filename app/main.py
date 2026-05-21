from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlmodel import select
from .database import init_db, get_session, engine, Session
from .models import Item, Activity, Trip
from .core import consolidate_items
import json
from pathlib import Path

app = FastAPI(title="Activity Packing Planner API")

frontend_dir = Path(__file__).parent.parent / "frontend"
app.mount("/frontend", StaticFiles(directory=str(frontend_dir)), name="frontend")


def seed_data(session):
    if session.exec(select(Item)).first():
        return

    seed_items = [
        Item(name="Socks", category="Clothing", default_quantity=1, quantity_unit="per_day", tags="clothing,essentials", notes="Pair per day"),
        Item(name="Toothbrush", category="Toiletries", default_quantity=1, quantity_unit="each", tags="toiletries", notes="One per traveller"),
        Item(name="Sunscreen", category="Toiletries", default_quantity=1, quantity_unit="per_trip", tags="skincare", notes="One bottle per traveller"),
    ]
    for item in seed_items:
        session.add(item)
    session.commit()

    default_activity = Activity(name="Weekend Travel", items_json=json.dumps([{"item_id": 1, "multiplier": 1}, {"item_id": 2, "multiplier": 1}, {"item_id": 3, "multiplier": 1}]))
    session.add(default_activity)
    session.commit()


@app.on_event("startup")
def on_startup():
    init_db()
    with Session(engine) as session:
        seed_data(session)


@app.get("/", response_class=FileResponse)
def index():
    return FileResponse(frontend_dir / "index.html")


@app.post("/items", response_model=Item)
def create_item(item: Item, session=Depends(get_session)):
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@app.get("/items")
def list_items(session=Depends(get_session)):
    items = session.exec(select(Item)).all()
    return items


@app.get("/items/{item_id}")
def get_item(item_id: int, session=Depends(get_session)):
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, updated: Item, session=Depends(get_session)):
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    item.name = updated.name
    item.category = updated.category
    item.default_quantity = updated.default_quantity
    item.quantity_unit = updated.quantity_unit
    item.tags = updated.tags
    item.notes = updated.notes
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@app.delete("/items/{item_id}")
def delete_item(item_id: int, session=Depends(get_session)):
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    session.delete(item)
    session.commit()
    return {"success": True}


@app.post("/activities", response_model=Activity)
def create_activity(activity: Activity, session=Depends(get_session)):
    session.add(activity)
    session.commit()
    session.refresh(activity)
    return activity


@app.get("/activities")
def list_activities(session=Depends(get_session)):
    activities = session.exec(select(Activity)).all()
    return activities


@app.get("/trips")
def list_trips(session=Depends(get_session)):
    trips = session.exec(select(Trip)).all()
    return trips


@app.get("/trips/{trip_id}")
def get_trip(trip_id: int, session=Depends(get_session)):
    trip = session.get(Trip, trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return trip


@app.get("/export/trip/{trip_id}")
def export_trip(trip_id: int, session=Depends(get_session)):
    trip = session.get(Trip, trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    data = {
        "id": trip.id,
        "name": trip.name,
        "duration_days": trip.duration_days,
        "travellers": trip.travellers,
        "activity_ids": json.loads(trip.activity_ids_json or '[]'),
        "items": json.loads(trip.items_json or '[]'),
        "reminders": json.loads(trip.reminders_json or '[]'),
        "created_at": trip.created_at.isoformat()
    }
    return data


@app.get("/export/items")
def export_items(session=Depends(get_session)):
    items = session.exec(select(Item)).all()
    return items


@app.get("/export/activities")
def export_activities(session=Depends(get_session)):
    activities = session.exec(select(Activity)).all()
    return activities


@app.get("/activities/{activity_id}")
def get_activity(activity_id: int, session=Depends(get_session)):
    activity = session.get(Activity, activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity


@app.put("/activities/{activity_id}", response_model=Activity)
def update_activity(activity_id: int, updated: Activity, session=Depends(get_session)):
    activity = session.get(Activity, activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    activity.name = updated.name
    activity.items_json = updated.items_json
    session.add(activity)
    session.commit()
    session.refresh(activity)
    return activity


@app.delete("/activities/{activity_id}")
def delete_activity(activity_id: int, session=Depends(get_session)):
    activity = session.get(Activity, activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    session.delete(activity)
    session.commit()
    return {"success": True}


@app.post("/trips")
def create_trip(payload: dict, session=Depends(get_session)):
    activity_ids = [int(aid) for aid in payload.get("activity_ids", [])]
    duration_days = int(payload.get("duration_days", 1))
    travellers = int(payload.get("travellers", 1))
    reminders = payload.get("reminders", [])
    save_trip = bool(payload.get("save", False))
    if not activity_ids:
        raise HTTPException(status_code=400, detail="No activity_ids provided")

    combined_items = []
    for aid in activity_ids:
        act = session.get(Activity, int(aid))
        if not act:
            continue
        items = json.loads(act.items_json or "[]")
        for it in items:
            combined_items.append(it)

    items_in_db = session.exec(select(Item)).all()
    item_defs = {i.id: {"default_quantity": i.default_quantity, "quantity_unit": i.quantity_unit, "name": i.name} for i in items_in_db}

    consolidated = consolidate_items(combined_items, item_defs, duration_days, travellers)
    response = {
        "name": payload.get("name"),
        "duration_days": duration_days,
        "travellers": travellers,
        "items": consolidated,
        "reminders": reminders,
        "activity_ids": activity_ids,
        "saved": False
    }

    if save_trip:
        trip = Trip(
            name=payload.get("name", "Untitled Trip"),
            duration_days=duration_days,
            travellers=travellers,
            activity_ids_json=json.dumps(activity_ids),
            items_json=json.dumps(consolidated),
            reminders_json=json.dumps(reminders),
        )
        session.add(trip)
        session.commit()
        session.refresh(trip)
        response["saved"] = True
        response["trip_id"] = trip.id

    return response
