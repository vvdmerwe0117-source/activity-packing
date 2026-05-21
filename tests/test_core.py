from app.core import compute_item_quantity, consolidate_items


def test_compute_item_quantity_per_day():
    q = compute_item_quantity(1, 'per_day', duration_days=3, travellers=2, multiplier=1)
    assert q == 6


def test_compute_item_quantity_per_trip():
    q = compute_item_quantity(2, 'per_trip', duration_days=5, travellers=3, multiplier=1)
    assert q == 6


def test_consolidate_items():
    items = [{'item_id': 1, 'multiplier': 1}, {'item_id': 1, 'multiplier': 0.5}, {'item_id': 2, 'multiplier': 1}]
    defs = {1: {'default_quantity': 1, 'quantity_unit': 'per_day', 'name': 'Socks'}, 2: {'default_quantity': 1, 'quantity_unit': 'each', 'name': 'Toothbrush'}}
    result = consolidate_items(items, defs, duration_days=2, travellers=1)
    # socks: (1 * 2 * 1 * (1+0.5)) = 3
    socks = next(x for x in result if x['item_id'] == 1)
    assert socks['computed_quantity'] == 3
