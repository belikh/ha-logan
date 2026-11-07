# Logan City Council

Home Assistant integration for **Logan City Council** — Queensland, Australia.

Everything in here comes from the council's public open data
(token-free, no API keys, no add-ons).

## What you get

- **All datasets** — every published dataset becomes a sensor showing its resource/feature count and source URL.
- **Waste collection days** (where openly published) — next bin collection + "put bins out tonight?" for one address/property.

## Data source

ArcGIS Hub / Datahub (47 catalogue items, token-free). Waste uses Logan_City_Bin_Collection FeatureServer (Formatted_Property_Address, Collection_Day, Recycling_Week).

## Install (HACS)

1. Add a custom repository: `https://github.com/belikh/ha-logan` as type **Integration**.
2. Install **Logan City Council** and restart Home Assistant.
3. Add the integration and choose: all layers / waste / single layer.

## Development

```bash
uv sync
uv run pytest
uv run ruff check .
uv run mypy
```

Licence: MIT. Data © Logan City Council (Creative Commons). Unofficial; not endorsed by the council.
