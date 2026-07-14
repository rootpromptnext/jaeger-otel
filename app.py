from flask import Flask
import os
import random
import time

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace import Status, StatusCode
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor

# -----------------------------------------------------------------------------
# OpenTelemetry Configuration
# -----------------------------------------------------------------------------

OTEL_ENDPOINT = os.getenv(
    "OTEL_EXPORTER_OTLP_ENDPOINT",
    "http://localhost:4318/v1/traces"
)

resource = Resource.create({
    "service.name": "python-flask-demo",
    "service.version": "1.0",
    "deployment.environment": "lab"
})

provider = TracerProvider(resource=resource)

provider.add_span_processor(
    BatchSpanProcessor(
        OTLPSpanExporter(
            endpoint=OTEL_ENDPOINT
        )
    )
)

trace.set_tracer_provider(provider)

tracer = trace.get_tracer(__name__)

# -----------------------------------------------------------------------------
# Flask Application
# -----------------------------------------------------------------------------

app = Flask(__name__)

FlaskInstrumentor().instrument_app(app)

# -----------------------------------------------------------------------------
# Routes
# -----------------------------------------------------------------------------

@app.route("/")
def home():

    with tracer.start_as_current_span("home-span") as span:

        span.set_attribute("app.route", "/")

        time.sleep(random.uniform(0.2, 1.0))

        return "Welcome to OpenTelemetry Demo\n"


@app.route("/hello")
def hello():

    with tracer.start_as_current_span("hello-span") as span:

        span.set_attribute("user.name", "student")

        span.set_attribute("lab.number", 2)

        time.sleep(random.uniform(0.1, 0.8))

        return "Hello OpenTelemetry\n"


@app.route("/slow")
def slow():

    with tracer.start_as_current_span("slow-operation") as span:

        span.set_attribute("operation.type", "slow")

        time.sleep(3)

        return "Slow API Completed\n"


@app.route("/error")
def error():

    with tracer.start_as_current_span("error-span") as span:

        try:

            time.sleep(0.5)

            raise Exception("Something went wrong")

        except Exception as ex:

            span.record_exception(ex)

            span.set_status(
                Status(StatusCode.ERROR, str(ex))
            )

            raise


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":

    print(f"OTLP Endpoint : {OTEL_ENDPOINT}")

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
