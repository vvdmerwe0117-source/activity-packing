# Activity Packing Planner — Detailed Specification

Derived from the decrypted challenge spec for Activity Packing Planner.

## 1. Overview
- **Title:** Activity Packing Planner
- **One-liner:** A reusable packing list manager that builds activity-based lists, calculates quantities per trip length, and tracks non-packing reminders.

## 2. Goals
- Provide users with reusable, activity-focused packing lists.
- Automate quantity calculations based on trip duration.
- Allow users to manage a master library of reusable items.
- Support non-packing reminders and checklist tracking.

## 3. Key Features
- Master Item Library: Add/edit/delete items that can be reused across lists. Each item includes name, category, default quantity (per day or per person), tags, and optional notes.
- Activity Lists: Create base lists for activities (e.g., golf, holiday). Lists reference items from the master library.
- Trip Scaling: For a given trip duration and number of travellers, automatically scale quantities (e.g., socks = 1 per day × travellers).
- Combine Lists: Merge multiple activity lists into a single trip list with de-duplicated items and summed quantities.
- Non-packing Reminders: Add reminders (e.g., "book house sitter") that appear alongside packing items but are tracked separately.
- Checklist Mode: Mark items/reminders as completed during packing. Save completed lists for reuse.
- Save & Share: Save lists to user account (or local file) and export as text/CSV.

## 4. User Stories
- As a user, I can create a new activity list (e.g., `Beach Day`) and add items from the master library.
- As a user, I can add a custom item and choose to save it to the master library.
- As a user, I can set trip duration and travellers and see scaled quantities instantly.
- As a user, I can merge two activity lists into one consolidated trip list.
- As a user, I can add non-packing reminders and check them off separately.

## 5. Data Model
- Item
  - id: uuid
  - name: string
  - category: string (optional)
  - default_quantity: number
  - quantity_unit: string (e.g., "per_day", "per_trip", "each")
  - tags: [string]
  - notes: string

- ActivityList
  - id: uuid
  - name: string
  - items: [{item_id, quantity_multiplier (default 1), notes}]

- Trip
  - id: uuid
  - name: string
  - start_date, end_date
  - duration_days: integer
  - travellers: integer
  - consolidated_items: [{item_id, computed_quantity, checked: bool}]
  - reminders: [{text, checked: bool}]

## 6. Quantity Rules
- `per_day` items: computed_quantity = default_quantity × duration_days × travellers
- `per_trip` items: computed_quantity = default_quantity × travellers
- `each` items: computed_quantity = default_quantity × travellers
- When combining lists, sum computed quantities for identical items; present merged notes.

## 7. UX / Screens
- Master Library Screen: Search, filter by category/tags, add/edit items, bulk-import.
- Activity List Editor: Add items from library, change multipliers, save as activity.
- Trip Builder: Select activities, set dates/travellers, preview computed list, reorder items, add reminders.
- Checklist View: Ticking items/reminders; progress indicator; Save completed list.

## 8. API (if server-backed)
- GET /items — list master items
- POST /items — create item
- PUT /items/{id} — update item
- GET /activities — list saved activities
- POST /activities — create activity list
- POST /trips — create trip and compute consolidated list

## 9. Acceptance Criteria
- Creating an activity and setting trip duration shows correct scaled quantities.
- Combining two activities merges identical items and sums quantities.
- Saving a custom item to the master library makes it available in other activities.

## 10. MVP Scope (Phase 1)
1. Master item library with add/edit/delete and tags.
2. Activity lists referencing library items.
3. Trip builder with duration/travellers scaling and consolidated list.
4. Checklist mode with save/export.

## 11. Next Tasks / Implementation Plan
- Frontend: simple web UI (React or plain HTML+JS) with screens for Library, Activities, Trip Builder, Checklist.
- Backend (optional): lightweight REST API (Flask/FastAPI) to persist items and lists.
- Storage: SQLite for server-backed, or local JSON for client-only MVP.
- Tests: unit tests for quantity calculation rules and list merging.

---
Source: extracted from [specifications/activity_packing_planner/challenge/decrypted_spec.txt](specifications/activity_packing_planner/challenge/decrypted_spec.txt#L1-L5)
