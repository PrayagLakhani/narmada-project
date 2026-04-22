import os
import time
import traceback
import requests

RENDER_URL = os.getenv("RENDER_URL", "https://narmada-project-qf03.onrender.com").rstrip("/")
POLL_SECONDS = int(os.getenv("WORKER_POLL_SECONDS", "30"))
WORKER_NAME = os.getenv("WORKER_NAME", "local-worker")


def process_job(job):
    job_type = (job.get("type") or "").strip().lower()

    if job_type == "clip_precip":
        from scripts.admin_raster_clip import admin_clip_precipitation_raster
        admin_clip_precipitation_raster()
        return {"message": "Precipitation clip completed"}

    if job_type == "clip_temp":
        from scripts.admin_raster_clip import admin_clip_temperature_raster
        admin_clip_temperature_raster()
        return {"message": "Temperature clip completed"}

    raise ValueError(f"Unsupported job type: {job_type}")


def claim_next_job():
    response = requests.post(
        f"{RENDER_URL}/claim-job",
        json={"worker": WORKER_NAME},
        timeout=30,
    )
    if response.status_code == 404:
        return None
    response.raise_for_status()
    return response.json()


def complete_job(job_id, status, result=None, error=None):
    payload = {
        "id": job_id,
        "status": status,
        "result": result,
        "error": error,
    }
    response = requests.post(f"{RENDER_URL}/complete-job", json=payload, timeout=60)
    response.raise_for_status()


def run_worker():
    print(f"Worker started. Render URL: {RENDER_URL}, poll every {POLL_SECONDS}s")

    while True:
        try:
            job = claim_next_job()

            if not job:
                time.sleep(POLL_SECONDS)
                continue

            job_id = job["id"]
            print(f"Processing job {job_id} ({job.get('type')})")

            try:
                result = process_job(job)
                complete_job(job_id, "done", result=result)
                print(f"Job {job_id} completed")
            except Exception as exc:
                error_text = f"{type(exc).__name__}: {exc}"
                complete_job(job_id, "failed", error=error_text)
                print(f"Job {job_id} failed: {error_text}")
                traceback.print_exc()

        except Exception as outer_exc:
            print(f"Worker loop error: {outer_exc}")
            traceback.print_exc()

        time.sleep(POLL_SECONDS)


if __name__ == "__main__":
    run_worker()
