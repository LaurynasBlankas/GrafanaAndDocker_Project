from fastapi import FastAPI
from prometheus_client import Counter, Histogram, make_asgi_app
import time

app = FastAPI()

REQUEST_COUNT = Counter("app_requests_total", "Total requests", ["endpoint"])
REQUEST_LATENCY = Histogram("app_request_latency_seconds", "Latency", ["endpoint"])
ERROR_COUNT = Counter("app_errors_total", "Total errors", ["endpoint"])


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


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/error")
def error(response: Response):
    ERROR_COUNT.labels(endpoint="/error").inc()
    REQUEST_COUNT.labels(endpoint="/error").inc()
    response.status_code = 500
    return {"message": "Something went wrong!"}


metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)
