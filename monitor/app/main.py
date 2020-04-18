import prometheus_client
from fastapi import FastAPI
from fastapi import Response
from prometheus_client import Counter
from prometheus_client import Summary
from prometheus_client.core import CollectorRegistry
from starlette.status import HTTP_201_CREATED
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from monitor.app.core.config import PROJECT_NAME
from monitor.app.core.models import CounterInput
from monitor.app.core.models import CounterResponse
from monitor.app.core.models import MetricsCounter


app = FastAPI(title=PROJECT_NAME)

temp_metric_storage = {}
temp_metric_storage["counter_producer"] = Counter(
    "counter_producer", "Number of produced Records"
)
temp_metric_storage["counter_consumer"] = Counter(
    "counter_consumer", "Number of consumed Records"
)


@app.get("/ping")
def ping():
    return {"ping": "pong!"}


@app.post(
    "/update/producer", response_model=CounterResponse, status_code=HTTP_201_CREATED
)
def update_producer_counter(payload: CounterInput) -> CounterResponse:

    temp_metric_storage["counter_producer"].inc(payload.increment_by)
    current_counter = temp_metric_storage["counter_producer"].collect()[0].samples[0][2]
    response = CounterResponse(
        incremented_by=payload.increment_by,
        current_counter=current_counter,
        status="HTTP_201_CREATED",
    )

    return response


@app.post(
    "/update/consumer", response_model=CounterResponse, status_code=HTTP_201_CREATED
)
def update_consumer_counter(payload: CounterInput) -> CounterResponse:

    temp_metric_storage["counter_consumer"].inc(payload.increment_by)
    current_counter = temp_metric_storage["counter_consumer"].collect()[0].samples[0][2]
    response = CounterResponse(
        incremented_by=payload.increment_by,
        current_counter=current_counter,
        status="HTTP_201_CREATED",
    )

    return response


@app.get("/metrics")
def show_metrics() -> MetricsCounter:
    current_counter_producer = (
        temp_metric_storage["counter_producer"].collect()[0].samples[0][2]
    )
    current_counter_consumer = (
        temp_metric_storage["counter_consumer"].collect()[0].samples[0][2]
    )

    response = MetricsCounter(
        produced_records=current_counter_producer,
        consumed_records=current_counter_consumer,
    )

    return response
