import requests
import time
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"
INTERVAL = 2
TIMEOUT = 5
RETRIES = 2

# endpoints com payload opcional
ENDPOINTS = [
    {"method": "GET", "path": "/"},
    {"method": "GET", "path": "/chain"},
    {"method": "GET", "path": "/mine"},
]


# =============================
# LOG FORMATTER
# =============================

def log(level, message):
    now = datetime.now().strftime("%H:%M:%S")
    print(f"[{now}] [{level}] {message}")


# =============================
# REQUEST HANDLER
# =============================

session = requests.Session()


def request_endpoint(method, path, payload=None):
    url = f"{BASE_URL}{path}"

    for attempt in range(RETRIES + 1):
        try:
            start = time.time()

            if method == "GET":
                response = session.get(url, timeout=TIMEOUT)

            elif method == "POST":
                response = session.post(url, json=payload, timeout=TIMEOUT)

            else:
                log("WARN", f"Unsupported method: {method}")
                return

            elapsed = round(time.time() - start, 3)

            log(
                "INFO",
                f"{method} {path} → {response.status_code} ({elapsed}s)"
            )

            try:
                data = response.json()
            except ValueError:
                data = response.text

            log("DATA", data)
            return

        except requests.ConnectionError:
            log("ERROR", f"{path} → Connection refused")

        except requests.Timeout:
            log("ERROR", f"{path} → Timeout")

        except requests.RequestException as e:
            log("ERROR", f"{path} → {e}")

        if attempt < RETRIES:
            log("RETRY", f"{path} retrying...")
            time.sleep(1)


# =============================
# MONITOR LOOP
# =============================

def monitor():
    log("SYSTEM", "Monitor started")

    while True:
        for endpoint in ENDPOINTS:
            request_endpoint(
                endpoint["method"],
                endpoint["path"],
                endpoint.get("payload")
            )

        time.sleep(INTERVAL)


if __name__ == "__main__":
    monitor()