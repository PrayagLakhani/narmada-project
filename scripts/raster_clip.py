import os
import subprocess
import tempfile


DATA_BASE_URL = os.getenv(
    "DATA_BASE_URL",
    "https://pub-7c568aa6f5ec40dbac09e26180370bdd.r2.dev"
).rstrip("/")


def clip_precipitation_raster():
    input_raster = f"{DATA_BASE_URL}/raster/2011_2023_Precipitation.tif"
    basin_geojson = f"{DATA_BASE_URL}/geojson/narmada.geojson"
    output_raster = f"{DATA_BASE_URL}/raster/precip_clipped.tif"

    valid_geojson = os.path.join(tempfile.gettempdir(), "narmada_valid.geojson")

    subprocess.run(
        ["ogr2ogr", "-makevalid", valid_geojson, basin_geojson],
        check=True
    )

    subprocess.run(
        [
            "gdalwarp",
            "-cutline", valid_geojson,
            "-crop_to_cutline",
            "-wm", "32",
            "-wo", "NUM_THREADS=2",
            "-of", "GTiff",
            "-co", "TILED=YES",
            "-co", "COMPRESS=DEFLATE",
            "-co", "BIGTIFF=YES",
            "-overwrite",
            input_raster,
            output_raster
        ],
        check=True
    )

    print("Precipitation raster clipped successfully")


def clip_temperature_raster():
    input_raster = f"{DATA_BASE_URL}/raster/2011_2023_Mean_Temperature.tif"
    basin_geojson = f"{DATA_BASE_URL}/geojson/narmada.geojson"
    output_raster = f"{DATA_BASE_URL}/raster/temp_clipped.tif"

    valid_geojson = os.path.join(tempfile.gettempdir(), "narmada_valid.geojson")

    subprocess.run(
        ["ogr2ogr", "-makevalid", valid_geojson, basin_geojson],
        check=True
    )

    subprocess.run(
        [
            "gdalwarp",
            "-cutline", valid_geojson,
            "-crop_to_cutline",
            "-wm", "32",
            "-wo", "NUM_THREADS=2",
            "-of", "GTiff",
            "-co", "TILED=YES",
            "-co", "COMPRESS=DEFLATE",
            "-co", "BIGTIFF=YES",
            "-overwrite",
            input_raster,
            output_raster
        ],
        check=True
    )

    print("Mean temperature raster clipped successfully")