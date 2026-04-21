import os
import sys
import re
import tempfile
import urllib.parse
import pandas as pd
import geopandas as gpd
import numpy as np
import rasterio
from rasterio.transform import from_origin
from rasterio.features import rasterize
from scipy.spatial.distance import cdist
from shapely.ops import unary_union
import requests

# Progress bar
try:
    from tqdm import tqdm
except:
    def tqdm(x, desc=""): return x

# =====================================================
# PATHS
# =====================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_URL = os.getenv("DATA_BASE_URL", "").rstrip("/")
if not BASE_URL:
    raise RuntimeError("DATA_BASE_URL environment variable is required.")

csv_relative_dir = "admin/display/streamflow"
buffer_relative_dir = "admin/display/shp"
output_folder = os.path.join(BASE_DIR, "data","admin","display", "streamflow", "output_streamflow_rasters")

year_input = int(sys.argv[1])
input_month=(sys.argv[2])

start_year = year_input
end_year = year_input
pixel_size = 30
power = 2

os.makedirs(output_folder, exist_ok=True)


def _data_url(relative_path):
    return f"{BASE_URL}/{relative_path.lstrip('/')}"


def _list_remote_files(relative_dir, extension):
    index_url = _data_url(relative_dir) + "/"
    try:
        response = requests.get(index_url, timeout=(10, 120))
        response.raise_for_status()
    except requests.exceptions.RequestException as exc:
        raise RuntimeError(
            f"Unable to list remote directory: {index_url}. "
            f"Check DATA_BASE_URL and DNS/network reachability."
        ) from exc
    hrefs = re.findall(r'href=["\']([^"\']+)["\']', response.text, flags=re.IGNORECASE)
    files = []
    for href in hrefs:
        parsed = urllib.parse.urlparse(href)
        candidate = parsed.path.split("/")[-1]
        if candidate.lower().endswith(extension.lower()):
            files.append(candidate)
    return sorted(set(files))


def _download_remote_file(relative_path, local_path):
    url = _data_url(relative_path)
    try:
        response = requests.get(url, stream=True, timeout=(10, 300))
        response.raise_for_status()
        with open(local_path, "wb") as out:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    out.write(chunk)
    except requests.exceptions.RequestException as exc:
        raise RuntimeError(
            f"Unable to download remote file: {url}. "
            f"Check DATA_BASE_URL and DNS/network reachability."
        ) from exc


def _prepare_remote_buffer_shapefile():
    temp_dir = tempfile.mkdtemp(prefix="narmada_buf_")
    base_name = "narmada_buffer_1000m"
    for ext in [".shp", ".shx", ".dbf", ".prj", ".cpg"]:
        rel = f"{buffer_relative_dir}/{base_name}{ext}"
        local = os.path.join(temp_dir, f"{base_name}{ext}")
        try:
            _download_remote_file(rel, local)
        except Exception:
            if ext in {".shp", ".shx", ".dbf"}:
                raise
    return os.path.join(temp_dir, f"{base_name}.shp")

# =====================================================
# STEP 1: READ ALL CSV FILES
# =====================================================
print("Reading streamflow CSV files...")

remote_csv_files = _list_remote_files(csv_relative_dir, ".csv")

if len(remote_csv_files) == 0:
    print("❌ No CSV files found")
    exit()

df_list = []
skipped_files = []

for csv_name in remote_csv_files:
    # Extract lon/lat from filename tail: ..._<lon>_<lat>.csv
    filename = os.path.basename(csv_name)
    stem = filename.replace(".csv", "")
    match = re.search(r"(-?\d+(?:\.\d+)?)_(-?\d+(?:\.\d+)?)$", stem)

    if match is None:
        skipped_files.append(f"{filename} (no lon/lat pattern)")
        continue

    lon = float(match.group(1))
    lat = float(match.group(2))

    if not (-180 <= lon <= 180 and -90 <= lat <= 90):
        skipped_files.append(f"{filename} (invalid lon/lat range)")
        continue

    temp_df = pd.read_csv(_data_url(f"{csv_relative_dir}/{filename}"))

    if "Year" not in temp_df.columns:
        skipped_files.append(f"{filename} (missing Year column)")
        continue

    # Convert wide → long
    temp_df = temp_df.melt(
        id_vars=["Year"],
        var_name="Month",
        value_name="Value"
    )

    temp_df["Latitude"] = lat
    temp_df["Longitude"] = lon

    df_list.append(temp_df)

if skipped_files:
    print("⚠ Skipped files:")
    for item in skipped_files:
        print(f"  - {item}")

if len(df_list) == 0:
    print("❌ No valid station CSV files found after filtering")
    exit(1)

# Combine all stations
df = pd.concat(df_list, ignore_index=True)

print("✅ Total records:", len(df))

# Clean
df.columns = df.columns.str.strip()
df = df.dropna(subset=["Latitude", "Longitude", "Value"])

# =====================================================
# STEP 2: GEO DATAFRAME
# =====================================================
print("Converting to GeoDataFrame...")

gdf = gpd.GeoDataFrame(
    df,
    geometry=gpd.points_from_xy(df["Longitude"], df["Latitude"]),
    crs="EPSG:4326"
).to_crs("EPSG:32644")

# =====================================================
# STEP 3: BUFFER
# =====================================================
print("Reading buffer shapefile...")

buffer_shp = _prepare_remote_buffer_shapefile()
buffer = gpd.read_file(buffer_shp).to_crs(gdf.crs)

# IMPORTANT: don't double buffer
buffer_union = unary_union(buffer.geometry)

# =====================================================
# STEP 4: GRID
# =====================================================
minx, miny, maxx, maxy = gpd.GeoSeries([buffer_union]).total_bounds

width = int((maxx - minx) / pixel_size)
height = int((maxy - miny) / pixel_size)

transform = from_origin(minx, maxy, pixel_size, pixel_size)

print(f"Raster size: {width} x {height}")

# =====================================================
# STEP 5: MASK
# =====================================================
print("Creating buffer mask...")

mask = rasterize(
    [(buffer_union, 1)],
    out_shape=(height, width),
    transform=transform,
    fill=0,
    dtype="uint8"
)

# =====================================================
# MONTHS
# =====================================================
months = [input_month]

# =====================================================
# STEP 6: IDW
# =====================================================
for year in range(start_year, end_year + 1):

    for month in months:

        print(f"\nProcessing {year}-{month}")

        subset = gdf[
            (gdf["Year"] == year) &
            (gdf["Month"] == month)
        ]

        if subset.empty:
            print("  No data")
            continue

        coords = np.array([(geom.x, geom.y) for geom in subset.geometry])
        values = subset["Value"].values

        out_path = os.path.join(
            output_folder,
            f"streamflow_{year}_{month}_30m.tif"
        )

        with rasterio.open(
            out_path,
            "w",
            driver="GTiff",
            height=height,
            width=width,
            count=1,
            dtype="float32",
            crs=gdf.crs,
            transform=transform,
            nodata=np.nan,
            compress="lzw"
        ) as dst:

            for ij, window in tqdm(dst.block_windows(), desc=f"{year}-{month}"):

                row_off = window.row_off
                col_off = window.col_off
                h = window.height
                w = window.width

                mask_chunk = mask[row_off:row_off+h, col_off:col_off+w]

                if not np.any(mask_chunk):
                    continue

                rows, cols = np.indices((h, w))
                rows += row_off
                cols += col_off

                xs, ys = rasterio.transform.xy(
                    transform, rows, cols, offset='center'
                )

                xs = np.array(xs).flatten()
                ys = np.array(ys).flatten()

                valid = mask_chunk.flatten() == 1
                if not np.any(valid):
                    continue

                target = np.column_stack((xs[valid], ys[valid]))

                # IDW
                dists = cdist(target, coords)
                dists[dists == 0] = 1e-10

                weights = 1 / (dists ** power)

                numerator = np.sum(weights * values, axis=1)
                denominator = np.sum(weights, axis=1)

                result = numerator / denominator

                block = np.full((h * w), np.nan, dtype="float32")
                block[valid] = result
                block = block.reshape((h, w))

                dst.write(block, 1, window=window)

        print("  ✔ Saved:", out_path)

print("\n✅ FINAL SUCCESS: Streamflow IDW rasters created!")