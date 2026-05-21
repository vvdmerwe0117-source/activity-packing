from typing import List, Dict


def compute_item_quantity(default_quantity: float, quantity_unit: str, duration_days: int, travellers: int, multiplier: float = 1.0) -> float:
    if quantity_unit == "per_day":
        return default_quantity * duration_days * travellers * multiplier
    elif quantity_unit in ("per_trip", "each"):
        return default_quantity * travellers * multiplier
    else:
        # fallback
        return default_quantity * travellers * multiplier


def consolidate_items(items: List[Dict], item_defs: Dict[int, Dict], duration_days: int, travellers: int) -> List[Dict]:
    """
    items: list of dicts with keys: item_id, multiplier
    item_defs: mapping item_id -> {default_quantity, quantity_unit, name}
    returns list of {item_id, name, computed_quantity}
    """
    agg = {}
    for entry in items:
        item_id = int(entry["item_id"])
        multiplier = float(entry.get("multiplier", 1.0))
        if item_id not in item_defs:
            continue
        defn = item_defs[item_id]
        qty = compute_item_quantity(defn.get("default_quantity", 1.0), defn.get("quantity_unit", "each"), duration_days, travellers, multiplier)
        agg.setdefault(item_id, {"item_id": item_id, "name": defn.get("name", ""), "computed_quantity": 0.0})
        agg[item_id]["computed_quantity"] += qty

    # round sensible
    result = []
    for v in agg.values():
        v["computed_quantity"] = int(v["computed_quantity"]) if v["computed_quantity"].is_integer() else round(v["computed_quantity"], 2)
        result.append(v)
    return result
