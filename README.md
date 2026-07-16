# Jaeger OpenTelemetry Flask Demo

This repository contains a simple Python Flask application instrumented with **OpenTelemetry**.  
The app generates traces and exports them to **Jaeger** using the OTLP HTTP exporter.

## Project Structure
- `app.py` — Flask application with OpenTelemetry instrumentation
- `requirements.txt` — Python dependencies
- `Dockerfile` — Container build instructions
- `deployment.yaml` — Kubernetes Deployment manifest
- `service.yaml` — Kubernetes Service manifest
- `venv/` — Local Python virtual environment (ignored in Git/Docker)

## Run Locally
1. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Export OTLP endpoint (port-forward or NodePort):
   ```bash
   export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318/v1/traces
   python app.py
   ```
4. Generate traffic:
   ```bash
   curl http://localhost:5000/
   curl http://localhost:5000/hello
   curl http://localhost:5000/error
   ```

## Build & Run with Docker
```bash
docker build -t flask-otel-demo .
docker run -p 5000:5000 \
  -e OTEL_EXPORTER_OTLP_ENDPOINT=http://<VM-Public-IP>:32113/v1/traces \
  flask-otel-demo
```

## Deploy to Kubernetes
1. Apply manifests:
   ```bash
   kubectl apply -f deployment.yaml
   kubectl apply -f service.yaml
   ```
2. Set OTLP endpoint inside `deployment.yaml`:
   ```yaml
   env:
     - name: OTEL_EXPORTER_OTLP_ENDPOINT
       value: "http://jaeger.observability.svc.cluster.local:4318/v1/traces"
   ```

## View Traces
- Jaeger UI: `http://<VM-Public-IP>:30686`
- Services: `flask-jaeger-otel`
- Endpoints: `/`, `/hello`, `/error`

##What You Learn
- How to instrument a Flask app with OpenTelemetry
- Export traces via OTLP
- Run locally, in Docker, and in Kubernetes
- Visualize distributed traces in Jaeger
