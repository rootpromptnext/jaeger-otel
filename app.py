import os
from flask import Flask
import random
import time

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor

# Read OTLP endpoint from environment variable
otlp_endpoint = os.getenv(
    "OTEL_EXPORTER_OTLP_ENDPOINT",
    "http://localhost:4318/v1/traces"   # default fallback
)

resource = Resource.create({"service.name": "python-flask-demo"})
provider = TracerProvider(resource=resource)
trace.set_tracer_provider(provider)

processor = BatchSpanProcessor(
    OTLPSpanExporter(endpoint=otlp_endpoint)
)
provider.add_span_processor(processor)

tracer = trace.get_tracer(__name__)
app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)

@app.route("/")
def home():
    with tracer.start_as_current_span("home-span"):
        time.sleep(random.uniform(0.2, 1.0))
        return "Welcome to OpenTelemetry Demo\n"

@app.route("/hello")
def hello():
    with tracer.start_as_current_span("hello-span"):
        time.sleep(random.uniform(0.1, 0.8))
        return "Hello OpenTelemetry\n"

@app.route("/error")
def error():
    with tracer.start_as_current_span("error-span"):
        time.sleep(0.5)
        raise Exception("Something went wrong")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
