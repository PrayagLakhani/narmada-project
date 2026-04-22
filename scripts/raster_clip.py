import os
import subprocess
import tempfile


BASE_DATA = r"O:\data"


def clip_precipitation_raster():
    input_raster = os.path.join(BASE_DATA, "raster", "2011_2023_Precipitation.tif")
    basin_geojson = os.path.join(BASE_DATA, "geojson", "narmada.geojson")
    output_raster = os.path.join(BASE_DATA, "raster", "precip_clipped.tif")

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
            "-multi",
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
    input_raster = os.path.join(BASE_DATA, "raster", "2011_2023_Mean_Temperature.tif")
    basin_geojson = os.path.join(BASE_DATA, "geojson", "narmada.geojson")
    output_raster = os.path.join(BASE_DATA, "raster", "temp_clipped.tif")

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
            "-multi",
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