"""Constants for the Logan integration."""

from __future__ import annotations

from datetime import timedelta

DOMAIN = "logan"

CONF_MODE = "mode"
CONF_ADDRESS = "address"
CONF_LAYER_TITLE = "layer_title"
CONF_SCAN_INTERVAL = "scan_interval_hours"
CONF_ZONE = "zone"
CONF_RADIUS_KM = "radius_km"

MODE_ALL_LAYERS = "all_layers"
MODE_WASTE = "waste"
MODE_SINGLE_LAYER = "single_layer"
MODE_NEARBY = "nearby"

CATALOGUE_URL = (
    "https://data-logancity.opendata.arcgis.com/api/search/v1/collections/dataset/items"
)
WASTE_URL = (
    "https://services5.arcgis.com/ZUCWDRj8F77Xo351/arcgis/rest/services/"
    "Logan_City_Bin_Collection/FeatureServer"
)
WASTE_TITLE = "Logan_City_Bin_Collection"

DEFAULT_SCAN_INTERVAL = timedelta(hours=6)
DEFAULT_ZONE = "zone.home"
DEFAULT_RADIUS_KM = 2.0
MIN_SCAN_INTERVAL_HOURS = 1
MAX_SCAN_INTERVAL_HOURS = 48

ATTR_LAYER_TITLE = "layer_title"
ATTR_FEATURE_COUNT = "feature_count"
ATTR_SOURCE_URL = "source_url"
ATTR_LAST_UPDATED = "last_updated"
