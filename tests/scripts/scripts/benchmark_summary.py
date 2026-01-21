import time
import statistics
import requests

URL = "http://127.0.0.1:8000/summary?month=2026-01"

def main(runs: int = 30):
    times = []
    for _ in range(runs):
        t0 = time.perf_counter()
        r = requests.get(URL)
        r.raise_for_status()
        times.append((time.perf_counter() - t0) * 1000)

    print(f"p50={statistics.median(times):.1f} ms")
    print(f"p95={statistics.quantiles(times, n=20)[18]:.1f} ms")
    print(f"min={min(times):.1f} ms, max={max(times):.1f} ms")

if __name__ == "__main__":
    main(30)
