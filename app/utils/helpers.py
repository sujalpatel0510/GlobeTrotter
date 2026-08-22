import os
import uuid
from pathlib import Path
from werkzeug.utils import secure_filename
from flask import current_app
from PIL import Image


def allowed_file(filename):
    """Check if uploaded file has an allowed image extension."""
    if not filename or '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    return ext in current_app.config.get('ALLOWED_EXTENSIONS', {'png', 'jpg', 'jpeg', 'gif', 'webp'})


def save_uploaded_image(file, subfolder='avatars', max_dim=800):
    """Saves and optionally resizes an uploaded image safely."""
    if not file or file.filename == '':
        return None

    if not allowed_file(file.filename):
        return None

    filename = secure_filename(file.filename)
    ext = filename.rsplit('.', 1)[1].lower()
    unique_filename = f"{uuid.uuid4().hex}.{ext}"

    upload_dir = Path(current_app.config['UPLOAD_FOLDER']) / subfolder
    upload_dir.mkdir(parents=True, exist_ok=True)
    file_path = upload_dir / unique_filename

    try:
        # Resize image for fast web serving
        img = Image.open(file)
        img.thumbnail((max_dim, max_dim))
        img.save(file_path)
        return f"uploads/{subfolder}/{unique_filename}"
    except Exception as e:
        current_app.logger.error(f"Error saving image: {e}")
        # Fallback to direct save
        file.seek(0)
        file.save(file_path)
        return f"uploads/{subfolder}/{unique_filename}"
