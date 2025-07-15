import os
import shutil
from pathlib import Path
from fastapi import UploadFile

# Set base path for voice storage
BASE = Path("core/data/voices")
BASE.mkdir(parents=True, exist_ok=True)

# Register: Save voice sample to voices directory
async def save_voice_register(username: str, password: str, audio: UploadFile):
    user_dir = BASE / username
    user_dir.mkdir(exist_ok=True)

    audio_path = user_dir / f"{username}.wav"

    with open(audio_path, "wb") as buffer:
        shutil.copyfileobj(audio.file, buffer)

    return str(audio_path)

# Login: Compare uploaded voice with stored sample
async def verify_voice_login(username: str, audio: UploadFile) -> bool:
    user_dir = BASE / username
    stored_audio_path = user_dir / f"{username}.wav"

    if not stored_audio_path.exists():
        return False

    temp_path = f"core/temp_uploads/{username}_temp.wav"

    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(audio.file, buffer)

    # For now, match voice by simple file size comparison (mock)
    try:
        return os.path.getsize(temp_path) == os.path.getsize(stored_audio_path)
    finally:
        os.remove(temp_path)
