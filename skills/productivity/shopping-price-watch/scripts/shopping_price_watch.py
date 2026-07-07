#!/usr/bin/env python3
"""Local shopping list and price-history tracker for Hermes."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any


STATE_VERSION = 1
WINDOWS = {"3mo": 90, "6mo": 180}
LATEST_BATCH_GAP = timedelta(minutes=5)


def _now() -> datetime:
    return datetime.now().astimezone()


def _now_iso() -> str:
    return _now().isoformat(timespec="seconds")


def _parse_dt(value: str) -> datetime:
    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    return datetime.fromisoformat(text)


def state_dir() -> Path:
    hermes_home = os.environ.get("HERMES_HOME")
    base = Path(hermes_home).expanduser() if hermes_home else Path.home() / ".hermes"
    return base / "state" / "shopping_price_watch"


def items_path() -> Path:
    return state_dir() / "items.json"


def history_path() -> Path:
    return state_dir() / "history.jsonl"


def _read_json(path: Path, default: dict[str, Any]) -> dict[str, Any]:
    if not path.exists():
        return default
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return data if isinstance(data, dict) else default


def _atomic_write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")
    tmp.replace(path)


def _append_jsonl(path: Path, record: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def _slugify(text: str) -> str:
    lowered = text.lower()
    slug = re.sub(r"[^a-z0-9가-힣]+", "-", lowered).strip("-")
    return slug[:64] or "item"


def load_items() -> dict[str, Any]:
    return _read_json(items_path(), {"version": STATE_VERSION, "items": []})


def save_items(data: dict[str, Any]) -> None:
    data["version"] = STATE_VERSION
    data.setdefault("items", [])
    _atomic_write_json(items_path(), data)


def _find_item(data: dict[str, Any], item_ref: str) -> dict[str, Any] | None:
    needle = item_ref.strip().lower()
    for item in data.get("items", []):
        if str(item.get("id", "")).lower() == needle:
            return item
        if str(item.get("name", "")).lower() == needle:
            return item
    return None


def add_item(
    name: str,
    query: str | None = None,
    item_id: str | None = None,
    notes: str | None = None,
    tags: list[str] | None = None,
) -> dict[str, Any]:
    data = load_items()
    now = _now_iso()
    ident = item_id.strip() if item_id else _slugify(name)
    item = _find_item(data, ident)
    if item is None:
        item = {
            "id": ident,
            "created_at": now,
        }
        data.setdefault("items", []).append(item)
    item.update(
        {
            "name": name,
            "query": query or name,
            "notes": notes or item.get("notes") or "",
            "tags": tags or item.get("tags") or [],
            "active": True,
            "updated_at": now,
        }
    )
    item.pop("removed_at", None)
    save_items(data)
    return item


def remove_item(item_ref: str) -> dict[str, Any]:
    data = load_items()
    item = _find_item(data, item_ref)
    if item is None:
        raise ValueError(f"item not found: {item_ref}")
    item["active"] = False
    item["removed_at"] = _now_iso()
    item["updated_at"] = item["removed_at"]
    save_items(data)
    return item


def load_active_items() -> list[dict[str, Any]]:
    return [item for item in load_items().get("items", []) if item.get("active", True)]


def _normalize_offer_price(
    price: float,
    currency: str,
    usd_krw: float | None,
) -> tuple[float | None, float | None]:
    curr = currency.upper()
    if curr == "KRW":
        price_krw = float(round(price))
        price_usd = round(price / usd_krw, 2) if usd_krw else None
    elif curr == "USD":
        price_usd = round(float(price), 2)
        price_krw = float(round(price * usd_krw)) if usd_krw else None
    else:
        raise ValueError("currency must be KRW or USD")
    return price_krw, price_usd


def record_offer(
    item_id: str,
    source: str,
    title: str,
    url: str,
    price: float,
    currency: str,
    usd_krw: float | None = None,
    captured_at: str | None = None,
    note: str | None = None,
) -> dict[str, Any]:
    data = load_items()
    item = _find_item(data, item_id)
    if item is None:
        raise ValueError(f"item not found: {item_id}")

    captured = captured_at or _now_iso()
    price_krw, price_usd = _normalize_offer_price(float(price), currency, usd_krw)
    record = {
        "item_id": item["id"],
        "item_name": item.get("name", item["id"]),
        "source": source,
        "title": title,
        "url": url,
        "raw_price": float(price),
        "raw_currency": currency.upper(),
        "price_krw": price_krw,
        "price_usd": price_usd,
        "usd_krw": usd_krw,
        "captured_at": captured,
        "note": note or "",
    }
    _append_jsonl(history_path(), record)
    return record


def load_history() -> list[dict[str, Any]]:
    path = history_path()
    if not path.exists():
        return []
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            text = line.strip()
            if not text:
                continue
            records.append(json.loads(text))
    return records


def _comparable_price(record: dict[str, Any]) -> float | None:
    value = record.get("price_krw")
    if value is None:
        value = record.get("price_usd")
    return float(value) if value is not None else None


def _latest_best(records: list[dict[str, Any]]) -> dict[str, Any] | None:
    if not records:
        return None
    ordered = sorted(records, key=lambda r: _parse_dt(str(r["captured_at"])), reverse=True)
    latest_records = [ordered[0]]
    previous_at = _parse_dt(str(ordered[0]["captured_at"]))
    for record in ordered[1:]:
        captured_at = _parse_dt(str(record["captured_at"]))
        if previous_at - captured_at > LATEST_BATCH_GAP:
            break
        latest_records.append(record)
        previous_at = captured_at
    priced = [(r, _comparable_price(r)) for r in latest_records]
    priced = [(r, p) for r, p in priced if p is not None]
    if not priced:
        return latest_records[0]
    return min(priced, key=lambda pair: pair[1])[0]


def _trend_for_window(
    records: list[dict[str, Any]],
    current: dict[str, Any] | None,
    now_dt: datetime,
    days: int,
) -> dict[str, Any]:
    if current is None:
        return {"status": "no_data", "points": 0}
    start = now_dt - timedelta(days=days)
    window_records = [
        r
        for r in records
        if _parse_dt(str(r["captured_at"])) >= start and _comparable_price(r) is not None
    ]
    if len(window_records) < 2:
        return {"status": "accumulating", "points": len(window_records)}

    current_price = _comparable_price(current)
    prices = [float(_comparable_price(r)) for r in window_records]
    window_min = min(prices)
    window_avg = sum(prices) / len(prices)
    if current_price is None:
        return {"status": "no_comparable_price", "points": len(window_records)}
    pct_from_min = ((current_price - window_min) / window_min * 100) if window_min else 0.0
    pct_vs_avg = ((current_price - window_avg) / window_avg * 100) if window_avg else 0.0
    status = "good" if current_price <= window_min * 1.02 else "normal"
    return {
        "status": status,
        "points": len(window_records),
        "min_price": round(window_min, 2),
        "avg_price": round(window_avg, 2),
        "pct_from_min": round(pct_from_min, 2),
        "pct_vs_avg": round(pct_vs_avg, 2),
    }


def build_report(now: str | None = None) -> dict[str, Any]:
    now_dt = _parse_dt(now) if now else _now()
    active = load_active_items()
    history = load_history()
    reports = []
    for item in active:
        item_records = [r for r in history if r.get("item_id") == item.get("id")]
        latest = _latest_best(item_records)
        windows = {
            label: _trend_for_window(item_records, latest, now_dt, days)
            for label, days in WINDOWS.items()
        }
        reports.append(
            {
                "id": item.get("id"),
                "name": item.get("name"),
                "query": item.get("query"),
                "latest_best": latest,
                "trend_windows": windows,
                "history_points": len(item_records),
            }
        )
    return {
        "generated_at": now_dt.isoformat(timespec="seconds"),
        "state_dir": str(state_dir()),
        "items": reports,
    }


def _print_json(data: Any) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True))


def _cmd_add(args: argparse.Namespace) -> None:
    item = add_item(
        name=args.name,
        query=args.query,
        item_id=args.id,
        notes=args.notes,
        tags=args.tag or [],
    )
    _print_json({"success": True, "item": item})


def _cmd_remove(args: argparse.Namespace) -> None:
    item = remove_item(args.item)
    _print_json({"success": True, "item": item})


def _cmd_list(args: argparse.Namespace) -> None:
    items = load_active_items() if args.active else load_items().get("items", [])
    _print_json({"success": True, "items": items})


def _cmd_record(args: argparse.Namespace) -> None:
    record = record_offer(
        item_id=args.item,
        source=args.source,
        title=args.title,
        url=args.url,
        price=args.price,
        currency=args.currency,
        usd_krw=args.usd_krw,
        captured_at=args.captured_at,
        note=args.note,
    )
    _print_json({"success": True, "record": record})


def _cmd_report(args: argparse.Namespace) -> None:
    _print_json(build_report(now=args.now))


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add", help="Add or reactivate a shopping-list item")
    add.add_argument("--id", help="Stable item id; defaults to a slug from name")
    add.add_argument("--name", required=True)
    add.add_argument("--query", help="Search query; defaults to name")
    add.add_argument("--notes", default="")
    add.add_argument("--tag", action="append", default=[])
    add.set_defaults(func=_cmd_add)

    remove = sub.add_parser("remove", help="Deactivate an item but keep history")
    remove.add_argument("item", help="Item id or exact item name")
    remove.set_defaults(func=_cmd_remove)

    list_cmd = sub.add_parser("list", help="List shopping-list items")
    list_cmd.add_argument("--active", action="store_true")
    list_cmd.set_defaults(func=_cmd_list)

    record = sub.add_parser("record", help="Record one observed offer")
    record.add_argument("--item", required=True, help="Item id")
    record.add_argument("--source", required=True)
    record.add_argument("--title", required=True)
    record.add_argument("--url", required=True)
    record.add_argument("--price", required=True, type=float)
    record.add_argument("--currency", required=True, choices=["KRW", "USD", "krw", "usd"])
    record.add_argument("--usd-krw", type=float)
    record.add_argument("--captured-at")
    record.add_argument("--note", default="")
    record.set_defaults(func=_cmd_record)

    report = sub.add_parser("report", help="Build JSON report from recorded history")
    report.add_argument("--now", help="ISO timestamp override for tests/backfills")
    report.set_defaults(func=_cmd_report)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        args.func(args)
    except Exception as exc:
        _print_json({"success": False, "error": str(exc)})
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
