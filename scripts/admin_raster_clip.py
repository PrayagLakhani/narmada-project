import os
import subprocess
import tempfile
import requests
import boto3

BASE_DATA = r"O:\data"


def r2_url(path):
    return f"{R2_PUBLIC}/{path.lstrip('/')}"



R2_PUBLIC = "https://pub-7c568aa6f5ec40dbac09e26180370bdd.r2.dev"
BUCKET = "narmada-project"

s3 = boto3.client(
    "s3",
    endpoint_url="https://0b772396ab70ea0cd591dfa63b52316b.r2.cloudflarestorage.com",
    # aws_access_key_id=os.environ["49d1528387711ac01001b28e753de9b8"],
    # aws_secret_access_key=os.environ["c5fc7491597429c1d73108ccf8d89754c1894523d4b80e21b3795eb9b296ea84"]
    aws_access_key_id=os.environ["R2_ACCESS_KEY"],
    aws_secret_access_key=os.environ["R2_SECRET_KEY"]
)

def download_file(url, local_path):
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception(f"Failed to download: {url}")
    with open(local_path, "wb") as f:
        f.write(r.content)

def admin_clip_precipitation_raster():
    # --- 1. Define R2 URLs ---
    input_url = f"{R2_PUBLIC}/admin/display/raster/2011_2023_Precipitation.tif"
    geojson_url = f"{R2_PUBLIC}/admin/display/geojson/narmada.geojson"

    # --- 2. Local temp paths ---
    tmp_dir = tempfile.gettempdir()
    local_raster = os.path.join(tmp_dir, "input_precip.tif")
    local_geojson = os.path.join(tmp_dir, "narmada.geojson")
    valid_geojson = os.path.join(tmp_dir, "narmada_valid.geojson")
    output_raster = os.path.join(tmp_dir, "precip_clipped.tif")

    # --- 3. Download from R2 ---
    download_file(input_url, local_raster)
    download_file(geojson_url, local_geojson)

    # --- 4. Make geometry valid ---
    subprocess.run(
        ["ogr2ogr", "-makevalid", valid_geojson, local_geojson],
        check=True
    )

    # --- 5. Clip raster ---
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
            "-overwrite",
            local_raster,
            output_raster
        ],
        check=True
    )

    # --- 6. Upload back to R2 ---
    s3.upload_file(
        output_raster,
        BUCKET,
        "admin/display/raster/precip_clipped.tif"
    )

    print("Precipitation raster clipped successfully")


def admin_clip_temperature_raster():

    input_url = f"{R2_PUBLIC}/admin/display/raster/2011_2023_Mean_Temperature.tif"
    geojson_url = f"{R2_PUBLIC}/admin/display/geojson/narmada.geojson"

    input_raster = _local_data_file("admin/display/raster/2011_2023_Mean_Temperature.tif")
    basin_geojson = _local_data_file("admin/display/geojson/narmada.geojson")
    output_raster = _local_data_file("admin/display/raster/temp_clipped.tif")
    os.makedirs(os.path.dirname(output_raster), exist_ok=True)

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



def collaborator_clip_precipitation_raster(collab_id):
    input_raster = _local_data_file(f"collaborator/{collab_id}/display/raster/precip_raster.tif")
    basin_geojson = _local_data_file(f"collaborator/{collab_id}/display/geojson/narmada.geojson")
    output_raster = _local_data_file(f"collaborator/{collab_id}/display/raster/precip_clipped.tif")
    os.makedirs(os.path.dirname(output_raster), exist_ok=True)

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


def collaborator_clip_temperature_raster(collab_id):
    input_raster = _local_data_file(f"collaborator/{collab_id}/display/raster/temp_raster.tif")
    basin_geojson = _local_data_file(f"collaborator/{collab_id}/display/geojson/narmada.geojson")
    output_raster = _local_data_file(f"collaborator/{collab_id}/display/raster/temp_clipped.tif")
    os.makedirs(os.path.dirname(output_raster), exist_ok=True)

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