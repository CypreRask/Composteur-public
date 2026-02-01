import os
import subprocess
import time
import sys

# Wrapper to run both API and Ingest in same console for easier view

print("--- Starting Compost Backend Services ---")

# 1. Start Ingest in Background Thread/Process
if sys.platform == "win32":
    # On Windows, using Popen to run ingest.py
    ingest = subprocess.Popen([sys.executable, "ingest.py"])
else:
    ingest = subprocess.Popen(["python3", "ingest.py"])

print("--- MQTT Ingest Started (PID: {}) ---".format(ingest.pid))

# 2. Run Uvicorn (Blocking)
# Using os.system to keep it simple and redirect output to this console
print("--- Starting API on Port 8085 ---")
os.system("uvicorn main:app --reload --host 0.0.0.0 --port 8085")

# When Uvicorn stops, kill ingest
ingest.terminate()
