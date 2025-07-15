from fastapi import FastAPI, Form, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from core.auth import register_user, authenticate_user
from core.voice_utils import save_voice_register, verify_voice_login

app = FastAPI()

# Serve static & frontend files
app.mount("/static", StaticFiles(directory="frontend"), name="static")
app.mount("/assets", StaticFiles(directory="assets"), name="assets")

@app.get("/", response_class=HTMLResponse)
async def get_register():
    return Path("frontend/register.html").read_text()

@app.get("/login", response_class=HTMLResponse)
async def get_login():
    return Path("frontend/login.html").read_text()

@app.get("/assignment", response_class=HTMLResponse)
async def get_assignment():
    return Path("frontend/assignment.html").read_text()

@app.post("/register")
async def post_register(
    username: str = Form(...),
    password: str = Form(...),
    audio: UploadFile = File(...)
):
    if password.strip() == "" or not audio.filename.endswith(".wav"):
        raise HTTPException(400, "Invalid data")
    await save_voice_register(username, password, audio)
    return RedirectResponse(url="/login", status_code=303)

@app.post("/login")
async def post_login(
    username: str = Form(...),
    password: str = Form(...),
    audio: UploadFile = File(...)
):
    if not authenticate_user(username, password):
        raise HTTPException(401, "Invalid username/password")

    ok = await verify_voice_login(username, audio)
    if not ok:
        raise HTTPException(403, "Voice mismatch")

    return RedirectResponse(url="/assignment", status_code=303)
