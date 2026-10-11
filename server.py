from fastapi import FastAPI
import subprocess
import sys
import os

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Laptop Voice Assistant Server Running"}


@app.get("/start")
def start_assistant():

    print("\nESP32 START command received!")

    project_folder = os.path.dirname(os.path.abspath(__file__))

    subprocess.Popen(
        [sys.executable, "full_voice_assistant.py"],
        cwd=project_folder
    )

    return {
        "status": "started",
        "message": "Voice Assistant Started"
    }
