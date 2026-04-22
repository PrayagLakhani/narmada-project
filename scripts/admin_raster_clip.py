import os
import subprocess
import tempfile
 

BASE_DATA = r"O:\data"


def _local_data_file(relative_path):
    return os.path.join(BASE_DATA, relative_path.replace("/", os.sep))


def admin_clip_precipitation_raster():
    input_raster = _local_data_file("admin/display/raster/2011_2023_Precipitation.tif")
    basin_geojson = _local_data_file("admin/display/geojson/narmada.geojson")
    output_raster = _local_data_file("admin/display/raster/precip_clipped.tif")
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