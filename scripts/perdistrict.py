import geopandas as gpd
import rasterio
from rasterio.mask import mask
from rasterio.errors import RasterioIOError
import numpy as np
import json
import os
import re
import pandas as pd
import tempfile
import hashlib
import requests
from shapely.geometry import Point


MONTH_ORDER = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
BASE_URL = "https://star-boys-revenues-conversation.trycloudflare.com/data"


def _data_url(relative_path):
    return f"{BASE_URL}/{relative_path.lstrip('/')}"


def _download_to_temp(relative_path, suffix):
    url = _data_url(relative_path)
    cache_key = hashlib.sha256(url.encode("utf-8")).hexdigest()[:16]
    cache_path = os.path.join(tempfile.gettempdir(), f"narmada_cache_{cache_key}{suffix}")

    if os.path.exists(cache_path) and os.path.getsize(cache_path) > 0:
        return cache_path

    tmp_part = f"{cache_path}.part"
    try:
        with requests.get(url, stream=True, timeout=(10, 600)) as response:
            response.raise_for_status()
            with open(tmp_part, "wb") as out:
                for chunk in response.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        out.write(chunk)
        os.replace(tmp_part, cache_path)
        return cache_path
    except Exception:
        if os.path.exists(tmp_part):
            os.remove(tmp_part)
        raise


def _remote_data_file(relative_path, suffix):
    return _download_to_temp(relative_path, suffix)


def _normalize_month_column(col_name):
    val = str(col_name).strip().lower()
    mapping = {
        "jan": "Jan", "january": "Jan",
        "feb": "Feb", "february": "Feb",
        "mar": "Mar", "march": "Mar",
        "apr": "Apr", "april": "Apr",
        "may": "May",
        "jun": "Jun", "june": "Jun",
        "jul": "Jul", "july": "Jul",
        "aug": "Aug", "august": "Aug",
        "sep": "Sep", "sept": "Sep", "september": "Sep",
        "oct": "Oct", "october": "Oct",
        "nov": "Nov", "november": "Nov",
        "dec": "Dec", "december": "Dec",
    }
    return mapping.get(val)


def _extract_lon_lat_from_filename(filename):
    # Parse coordinates from the filename tail to handle variable prefixes.
    match = re.search(r"(-?\d+(?:\.\d+)?)_(-?\d+(?:\.\d+)?)\.csv$", filename)
    if not match:
        return None
    try:
        return float(match.group(1)), float(match.group(2))
    except ValueError:
        return None


def _compute_parameter_means_for_district(base_dir, district_geom):
    display_dir = os.path.join(base_dir, "data", "admin", "display")
    if not os.path.exists(display_dir):
        return []

    folder_labels = {
        "precip": "Precipitation",
        "temp": "Temperature",
        "streamflow": "Streamflow",
        "waterlevel": "Water Level",
    }

    results = []

    for folder_name in sorted(os.listdir(display_dir)):
        folder_path = os.path.join(display_dir, folder_name)
        if not os.path.isdir(folder_path):
            continue

        csv_files = [
            f for f in os.listdir(folder_path)
            if f.lower().endswith(".csv")
            and not f.lower().startswith("sample")
            and "zone.identifier" not in f.lower()
        ]
        if not csv_files:
            continue

        station_files = []
        for file_name in csv_files:
            coords = _extract_lon_lat_from_filename(file_name)
            if not coords:
                continue
            lon, lat = coords
            point = Point(lon, lat)
            if district_geom.intersects(point):
                station_files.append(os.path.join(folder_path, file_name))

        if not station_files:
            results.append({
                "label": folder_labels.get(folder_name, folder_name.replace("_", " ").title()),
                "mean": None,
                "stations": 0,
                "records": 0,
                "year_min": None,
                "year_max": None,
                "months": [],
            })
            continue

        all_rows = []
        for csv_path in station_files:
            try:
                df = pd.read_csv(csv_path)
            except Exception:
                continue

            if df.empty:
                continue

            year_col = next((c for c in df.columns if str(c).strip().lower() == "year"), df.columns[0])
            local = pd.DataFrame()
            local["Year"] = pd.to_numeric(df[year_col], errors="coerce")

            month_cols = {}
            for col in df.columns:
                normalized = _normalize_month_column(col)
                if normalized:
                    month_cols[col] = normalized

            if not month_cols:
                continue

            for original_col, normalized_col in month_cols.items():
                local[normalized_col] = pd.to_numeric(df[original_col], errors="coerce")

            long_df = local.melt(id_vars=["Year"], var_name="Month", value_name="Value")
            long_df = long_df.dropna(subset=["Year", "Value"])

            if long_df.empty:
                continue

            long_df["Year"] = long_df["Year"].astype(int)
            all_rows.append(long_df)

        if not all_rows:
            results.append({
                "label": folder_labels.get(folder_name, folder_name.replace("_", " ").title()),
                "mean": None,
                "stations": len(station_files),
                "records": 0,
                "year_min": None,
                "year_max": None,
                "months": [],
            })
            continue

        combined = pd.concat(all_rows, ignore_index=True)

        month_set = sorted(set(combined["Month"].dropna().tolist()), key=lambda m: MONTH_ORDER.index(m))
        mean_val = float(combined["Value"].mean()) if not combined.empty else None

        results.append({
            "label": folder_labels.get(folder_name, folder_name.replace("_", " ").title()),
            "mean": mean_val,
            "stations": len(station_files),
            "records": int(len(combined)),
            "year_min": int(combined["Year"].min()) if not combined.empty else None,
            "year_max": int(combined["Year"].max()) if not combined.empty else None,
            "months": month_set,
        })

    return results

def mean_two_rasters_for_district_in_narmada(
    district_geojson="district_boundary.geojson",
    narmada_geojson="narmada.geojson",
    precip_raster="2011_2023_Precipitation.tif",
    temp_raster="2011_2023_Mean_Temperature.tif"
):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raster_dir = os.path.join(BASE_DIR, "data", "admin", "display", "raster")

    def resolve_raster_path(primary_name, alternatives=None):
        candidates = [primary_name] + (alternatives or [])
        for name in candidates:
            rel = f"admin/display/raster/{name}"
            try:
                return _download_to_temp(rel, ".tif")
            except Exception:
                continue
        raise FileNotFoundError(f"Raster not available at data server: {candidates}")

    district_geojson = _remote_data_file(
        f"admin/display/geojson/{district_geojson}",
        ".geojson",
    )
    narmada_geojson = _remote_data_file(
        f"admin/display/geojson/{narmada_geojson}",
        ".geojson",
    )
    precip_raster = resolve_raster_path(precip_raster)
    temp_raster = resolve_raster_path(temp_raster, ["2011_2023_MEAN_TEMPERATURE.tif"])

    districts = gpd.read_file(district_geojson).to_crs("EPSG:4326")
    narmada = gpd.read_file(narmada_geojson).to_crs("EPSG:4326")
    narmada_geom = narmada.geometry.union_all()

    district_name = input("").strip().upper()
    district = districts[districts["District"].str.upper() == district_name]

    if district.empty:
        print("District not found.")
        return

    district_narmada = district.geometry.intersection(narmada_geom)
    if district_narmada.is_empty.all():
        print("District has no area inside Narmada basin.")
        return

    shapes = [json.loads(district_narmada.to_json())["features"][0]["geometry"]]

    def compute_mean(raster_path):
        with rasterio.open(raster_path) as src:
            clipped, _ = mask(src, shapes, crop=True, nodata=src.nodata)
            data = clipped[0]

            if src.nodata is not None:
                data = data[data != src.nodata]

            data = data[~np.isnan(data)]
            if data.size == 0:
                return None

            return data.mean()

    try:
        mean_precip = compute_mean(precip_raster)
        mean_temp = compute_mean(temp_raster)
    except RasterioIOError as e:
        print(f"Raster file not found or unreadable: {e}")
        return
    except ValueError:
        print("Raster does not overlap after intersection.")
        return

    print(f"Mean Precipitation (2011-2023 raster): {mean_precip:.2f}")
    print(f"Mean Temperature (2011-2023 raster): {mean_temp:.2f} °C")

    param_stats = _compute_parameter_means_for_district(BASE_DIR, district_narmada.iloc[0])

    if param_stats:
        print("\nAll Parameters (all available years/months from data/admin/display):")

    for entry in param_stats:
        label = entry["label"]
        mean_val = entry["mean"]
        stations = entry["stations"]
        records = entry["records"]
        year_min = entry["year_min"]
        year_max = entry["year_max"]
        months = ", ".join(entry["months"]) if entry["months"] else "N/A"

        if mean_val is None:
            print(f"Mean {label}: No data (stations={stations})")
            continue

        print(
            f"Mean {label}: {mean_val:.2f} "
            f"[stations={stations}, records={records}, years={year_min}-{year_max}, months={months}]"
        )


if __name__ == "__main__":
    mean_two_rasters_for_district_in_narmada()