import requests
import time
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"

ENDPOINTS = [
    ("GET", "/"),
    ("GET", "/chain"),
    ("GET", "/mine"),
]

INTERVAL = 2


def log(level, message):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [{level}] {message}")


def request_endpoint(method, path):
    url = f"{BASE_URL}{path}"
    start = time.time()

    if method == "GET":
        response = requests.get(url, timeout=5)
    elif method == "POST":
        response = requests.post(url, timeout=5)
    else:
        return

    elapsed = round(time.time() - start, 3)

    log("INFO", f"{method} {path} STATUS={response.status_code} TIME={elapsed}s")

    try:
        log("DATA", response.json())
    except:
        log("DATA", response.text)


def monitor():
    while True:
        for method, path in ENDPOINTS:
            try:
                request_endpoint(method, path)
            except requests.ConnectionError:
                log("ERROR", f"{path} Connection refused")
            except requests.Timeout:
                log("ERROR", f"{path} Request timeout")
            except Exception as e:
                log("ERROR", f"{path} {str(e)}")

        time.sleep(INTERVAL)


if __name__ == "__main__":
    log("SYSTEM", "Monitor started")
    monitor()