from fastapi import FastAPI
from prometheus_client import Counter, Histogram, make_asgi_app
import time

app = FastAPI()

REQUEST_COUNT = Counter("app_requests_total", "Total requests", ["endpoint"])
REQUEST_LATENCY = Histogram("app_request_latency_seconds", "Latency", ["endpoint"])

@app.get("/")
def root():
    REQUEST_COUNT.labels(endpoint="/").inc()
    return {"message": "Hello from Docker!"}

@app.get("/slow")
def slow():
    start = time.time()
    time.sleep(0.5)
    REQUEST_LATENCY.labels(endpoint="/slow").observe(time.time() - start)
    return {"message": "That was slow"}

metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)