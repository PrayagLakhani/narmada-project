import os
import subprocess
import tempfile
import hashlib
import requests


BASE_URL = os.getenv("DATA_BASE_URL", "https://star-boys-revenues-conversation.trycloudflare.com/data").rstrip("/")


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
    except requests.exceptions.RequestException as exc:
        if os.path.exists(tmp_part):
            os.remove(tmp_part)
        raise RuntimeError(
            f"Unable to download remote data file: {url}. "
            f"Check DATA_BASE_URL and DNS/network reachability."
        ) from exc


def _remote_data_file(relative_path, suffix):
    return _download_to_temp(relative_path, suffix)


def admin_clip_precipitation_raster():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    input_raster = _remote_data_file(
        "admin/display/raster/2011_2023_Precipitation.tif",
        ".tif",
    )
    basin_geojson = _remote_data_file(
        "admin/display/geojson/narmada.geojson",
        ".geojson",
    )
    output_raster = os.path.join(BASE_DIR, "data", "admin","display", "raster", "precip_clipped.tif")
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
            "-wm", "128",
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


def admin_clip_temperature_raster():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    input_raster = _remote_data_file(
        "admin/display/raster/2011_2023_Mean_Temperature.tif",
        ".tif",
    )
    basin_geojson = _remote_data_file(
        "admin/display/geojson/narmada.geojson",
        ".geojson",
    )
    output_raster = os.path.join(BASE_DIR, "data","admin","display", "raster", "temp_clipped.tif")
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
            "-wm", "128",
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
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    input_raster = _remote_data_file(
        f"collaborator/{collab_id}/display/raster/precip_raster.tif",
        ".tif",
    )
    basin_geojson = _remote_data_file(
        f"collaborator/{collab_id}/display/geojson/narmada.geojson",
        ".geojson",
    )
    output_raster = os.path.join(BASE_DIR, "data", "collaborator",collab_id,"display", "raster", "precip_clipped.tif")
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
            "-wm", "128",
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
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    input_raster = _remote_data_file(
        f"collaborator/{collab_id}/display/raster/temp_raster.tif",
        ".tif",
    )
    basin_geojson = _remote_data_file(
        f"collaborator/{collab_id}/display/geojson/narmada.geojson",
        ".geojson",
    )
    output_raster = os.path.join(BASE_DIR, "data","collaborator",collab_id,"display", "raster", "temp_clipped.tif")
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
            "-wm", "128",
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