import os

from celery import Celery
from PIL import Image

from core.config import REDIS_URL, UPLOAD_FOLDER, PROCESSED_FOLDER


celery = Celery(
    "tasks",
    broker=REDIS_URL,
    backend=REDIS_URL
)

celery.conf.worker_pool = "solo"


@celery.task
def process_file(file_name: str):
    """Process an image file: convert to JPEG and compress."""
    input_path = os.path.join(UPLOAD_FOLDER, file_name)
    output_path = os.path.join(PROCESSED_FOLDER, file_name)

    if not os.path.exists(input_path):
        return f"Error: File {input_path} not found!"

    try:
        with Image.open(input_path) as img:
            img = img.convert('RGB')
            img.save(output_path, 'JPEG', quality=70)
        return f"File {file_name} successfully processed!"

    except Exception as e:
        return f"Error processing {file_name}: {str(e)}"


if __name__ == "__main__":
    celery.worker_main()
