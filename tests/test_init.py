"""Tests for the Logan integration."""

from datetime import date

from custom_components.logan.client import (
    build_where_clause,
    parse_catalogue,
    parse_waste_property,
)
from custom_components.logan.waste import (
    next_collection_date,
    put_out_tonight,
)

CATALOGUE_FIXTURE = {
    "features": [
        {
            "properties": {
                "title": "Logan_City_Bin_Collection",
                "url": "https://services5.arcgis.com/ZUCWDRj8F77Xo351/arcgis/rest/services/Logan_City_Bin_Collection/FeatureServer",
                "snippet": "Bin days",
            }
        },
        {
            "properties": {
                "title": "Logan_City_Council_Parks",
                "url": "https://services5.arcgis.com/x/arcgis/rest/services/Logan_City_Council_Parks/FeatureServer/0",
            }
        },
        {"properties": {"title": "", "url": ""}},
    ]
}

WASTE_FIXTURE = {
    "features": [
        {
            "attributes": {
                "Formatted_Property_Address": "53 Wendron Street, ROCHEDALE SOUTH QLD 4123",
                "Collection_Day": "MON",
                "Recycling_Week": "Week 1",
                "Suburb": "ROCHEDALE SOUTH",
            }
        }
    ]
}


def test_parse_catalogue_skips_empty_and_sorts() -> None:
    layers = parse_catalogue(CATALOGUE_FIXTURE)
    assert len(layers) == 2
    assert layers[0].title == "Logan_City_Bin_Collection"
    assert layers[1].layer == 0
    assert layers[1].query_url().endswith("/FeatureServer/0/query")


def test_build_where_clause_escapes_quotes() -> None:
    clause = build_where_clause("5 O'Brien St")
    assert "FORMATTED_PROPERTY_ADDRESS" in clause.upper()
    assert "''" in clause


def test_parse_waste_property() -> None:
    result = parse_waste_property(WASTE_FIXTURE)
    assert result is not None
    assert result["Collection_Day"] == "MON"
    assert parse_waste_property({"features": []}) is None


def test_next_collection_date() -> None:
    assert next_collection_date("MON", date(2026, 11, 7)) == date(2026, 11, 9)
    assert next_collection_date("saturday", date(2026, 11, 7)) == date(2026, 11, 7)
    assert next_collection_date("BOGUS", date(2026, 11, 7)) is None


def test_put_out_tonight() -> None:
    assert put_out_tonight("MON", date(2026, 11, 8)) is True
    assert put_out_tonight("MON", date(2026, 11, 7)) is False
