<p align="right">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/belikh/design/latest/packages/graphics/logo/jupiter-logo-dark.svg">
    <img alt="jupiter.au" src="https://raw.githubusercontent.com/belikh/design/latest/packages/graphics/logo/jupiter-logo-light.svg" width="260">
  </picture>
</p>

# Logan City Council

Home Assistant integration that turns datasets from the Logan City Council open data hub into sensors. It needs no API key.

<br>

---

<br>

## Install

1. In HACS, add a custom repository: `https://github.com/belikh/ha-logan`, type **Integration**.
2. Install **Logan City Council** and restart Home Assistant.
3. Go to **Settings > Devices & Services > Add integration** and pick **Logan City Council**.

<br>

## Use

The integration reads the council's ArcGIS Hub catalogue (`data-logancity.opendata.arcgis.com`) and creates one sensor per dataset. The state is the number of features in the dataset. The attributes are `layer_title`, `source_url` and `feature_count`.

The catalogue is filtered to datasets that change over time. Datasets whose titles do not match the integration's list of live-data keywords, and historical datasets, are skipped.

<br>

## Configuration

The refresh interval is set at setup and can be changed later under **Configure** on the integration card. It defaults to 6 hours and accepts 1 to 48.

<br>

## Develop

```sh
uv sync
uv run pytest
uv run ruff check .
uv run mypy
```

<br>

## Licence

MIT. Data (c) Logan City Council, Creative Commons. Unofficial; not endorsed by the council.

<br>

<p align="right"><sub>jupiter.au</sub></p>
