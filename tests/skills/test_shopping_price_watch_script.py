import importlib.util
import re
from pathlib import Path

import yaml


SCRIPT_PATH = (
    Path(__file__).resolve().parents[2]
    / "skills"
    / "productivity"
    / "shopping-price-watch"
    / "scripts"
    / "shopping_price_watch.py"
)
SKILL_PATH = SCRIPT_PATH.parents[1] / "SKILL.md"


def load_module():
    spec = importlib.util.spec_from_file_location("shopping_price_watch", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_skill_description_matches_hardline_format():
    content = SKILL_PATH.read_text(encoding="utf-8")
    match = re.search(r"^---\n(.*?)\n---", content, re.DOTALL)
    assert match, "SKILL.md missing YAML frontmatter"
    frontmatter = yaml.safe_load(match.group(1))

    desc = frontmatter["description"]
    assert len(desc) <= 60, f"description is {len(desc)} chars: {desc!r}"
    assert desc.endswith(".")


def test_add_and_remove_item_uses_profile_state_dir(tmp_path, monkeypatch):
    monkeypatch.setenv("HERMES_HOME", str(tmp_path))
    mod = load_module()

    added = mod.add_item(
        name="AirPods Pro latest revision",
        query="AirPods Pro latest revision",
        item_id="airpods-pro-latest",
        notes="latest Apple earbuds revision",
    )
    assert added["id"] == "airpods-pro-latest"

    state = mod.load_items()
    assert state["items"][0]["name"] == "AirPods Pro latest revision"
    assert state["items"][0]["active"] is True

    removed = mod.remove_item("airpods-pro-latest")
    assert removed["id"] == "airpods-pro-latest"
    assert removed["active"] is False

    active_items = mod.load_active_items()
    assert active_items == []


def test_report_flags_latest_price_as_good_against_3mo_and_6mo_history(tmp_path, monkeypatch):
    monkeypatch.setenv("HERMES_HOME", str(tmp_path))
    mod = load_module()

    mod.add_item(
        name="iPhone latest Pro 256GB",
        query="iPhone latest Pro 256GB",
        item_id="iphone-pro-256",
    )
    mod.record_offer(
        item_id="iphone-pro-256",
        source="Amazon",
        title="iPhone Pro 256GB historical",
        url="https://example.com/old",
        price=1200,
        currency="USD",
        usd_krw=1400,
        captured_at="2026-04-01T00:00:00+09:00",
    )
    mod.record_offer(
        item_id="iphone-pro-256",
        source="Amazon",
        title="iPhone Pro 256GB current",
        url="https://example.com/current",
        price=950,
        currency="USD",
        usd_krw=1400,
        captured_at="2026-05-29T06:00:00+09:00",
    )

    report = mod.build_report(now="2026-05-29T06:05:00+09:00")
    item_report = report["items"][0]

    assert item_report["latest_best"]["price_usd"] == 950.0
    assert item_report["trend_windows"]["3mo"]["status"] == "good"
    assert item_report["trend_windows"]["6mo"]["status"] == "good"


def test_latest_best_compares_offers_from_same_collection_batch(tmp_path, monkeypatch):
    monkeypatch.setenv("HERMES_HOME", str(tmp_path))
    mod = load_module()

    mod.add_item(
        name="AirPods Pro latest revision",
        query="AirPods Pro latest revision",
        item_id="airpods-pro-latest",
    )
    mod.record_offer(
        item_id="airpods-pro-latest",
        source="Amazon",
        title="AirPods Pro 3 cheaper offer",
        url="https://example.com/amazon",
        price=199,
        currency="USD",
        usd_krw=1500,
        captured_at="2026-05-29T06:00:01+09:00",
    )
    mod.record_offer(
        item_id="airpods-pro-latest",
        source="Coupang",
        title="AirPods Pro 3 later offer",
        url="https://example.com/coupang",
        price=339790,
        currency="KRW",
        usd_krw=1500,
        captured_at="2026-05-29T06:00:05+09:00",
    )

    report = mod.build_report(now="2026-05-29T06:05:00+09:00")
    item_report = report["items"][0]

    assert item_report["latest_best"]["source"] == "Amazon"
    assert item_report["latest_best"]["price_usd"] == 199.0


def test_latest_best_ignores_older_collection_batch_even_within_30_minutes(tmp_path, monkeypatch):
    monkeypatch.setenv("HERMES_HOME", str(tmp_path))
    mod = load_module()

    mod.add_item(
        name="AirPods Pro latest revision",
        query="AirPods Pro latest revision",
        item_id="airpods-pro-latest",
    )
    mod.record_offer(
        item_id="airpods-pro-latest",
        source="Stale Tracker",
        title="AirPods Pro stale cheaper offer",
        url="https://example.com/stale",
        price=199,
        currency="USD",
        usd_krw=1500,
        captured_at="2026-05-29T06:00:00+09:00",
    )
    mod.record_offer(
        item_id="airpods-pro-latest",
        source="Coupang",
        title="AirPods Pro current batch",
        url="https://example.com/current",
        price=335000,
        currency="KRW",
        usd_krw=1500,
        captured_at="2026-05-29T06:09:00+09:00",
    )

    report = mod.build_report(now="2026-05-29T06:10:00+09:00")
    item_report = report["items"][0]

    assert item_report["latest_best"]["source"] == "Coupang"


def test_report_marks_trend_as_accumulating_until_two_points_exist(tmp_path, monkeypatch):
    monkeypatch.setenv("HERMES_HOME", str(tmp_path))
    mod = load_module()

    mod.add_item(
        name="Galaxy Ultra latest 256GB",
        query="Galaxy Ultra latest 256GB",
        item_id="galaxy-ultra-256",
    )
    mod.record_offer(
        item_id="galaxy-ultra-256",
        source="Naver Shopping",
        title="Galaxy Ultra latest 256GB",
        url="https://example.com/galaxy",
        price=1700000,
        currency="KRW",
        captured_at="2026-05-29T06:00:00+09:00",
    )

    report = mod.build_report(now="2026-05-29T06:05:00+09:00")
    item_report = report["items"][0]

    assert item_report["trend_windows"]["3mo"]["status"] == "accumulating"
    assert item_report["trend_windows"]["6mo"]["status"] == "accumulating"
