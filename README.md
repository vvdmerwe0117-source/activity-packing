# Activity Packing Planner (work in progress)

This repository contains a FastAPI backend, SQLite storage, and a Vue + Tailwind frontend loaded from public CDNs.

## Run locally

1. Create a virtualenv and install dependencies:

```bash
python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows PowerShell
.venv\Scripts\Activate.ps1
# Windows CMD
.venv\Scripts\activate.bat
pip install -r requirements.txt
```

2. Start the app:

```bash
uvicorn app.main:app --reload
```

3. Open the frontend at:

```text
http://localhost:8000
```

## Features

- Full CRUD for packing items and activity lists
- Trip builder with quantity scaling by duration and travellers
- Reminders persistence for saved trips
- Saved trip storage and export to JSON
- Seed data loaded automatically on first startup

## API endpoints

- `GET /items` — list saved items
- `POST /items` — create item
- `PUT /items/{id}` — update item
- `DELETE /items/{id}` — delete item
- `GET /activities` — list activity lists
- `POST /activities` — create activity
- `PUT /activities/{id}` — update activity
- `DELETE /activities/{id}` — delete activity
- `POST /trips` — compute a trip checklist and optionally save it with `save: true`
- `GET /trips` — list saved trips
- `GET /export/trip/{id}` — export saved trip JSON
- `GET /export/items` — export item library
- `GET /export/activities` — export activity library

## Container run

Build and start the single container app:

```bash
docker build -t activity-packing .
docker run --rm -p 8000:8000 activity-packing
```

Then open:

```text
http://localhost:8000
```
