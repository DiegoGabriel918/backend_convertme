from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()
UPLOAD_FOLDER = str(BASE_DIR / "uploads")
TEMP_UPLOAD_FOLDER = str(BASE_DIR / "temp_uploads")

Path(UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)
Path(TEMP_UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)
