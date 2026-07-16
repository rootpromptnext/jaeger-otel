# Flask Jaeger OpenTelemetry

A simple Python Flask application instrumented with **OpenTelemetry** and exporting traces to **Jaeger** using the **OTLP HTTP Exporter**.

## Project Structure

```
.
├── app.py
├── requirements.txt
├── Dockerfile
├── deployment.yaml
└── README.md
```

---

# Prerequisites

- Python 3.12+
- Docker
- Kubernetes (MicroK8s)
- Jaeger with OTLP enabled

---

# Install Python Dependencies

```bash
python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt
```

---

# Run the Application

Set the OTLP endpoint.

```bash
export OTEL_EXPORTER_OTLP_ENDPOINT=http://<JAEGER_HOST>:4318/v1/traces
```

Example

```bash
export OTEL_EXPORTER_OTLP_ENDPOINT=http://192.168.1.10:32221/v1/traces
```

Run the application

```bash
python3 app.py
```

Application URL

```
http://localhost:5000
```

Test

```bash
curl http://localhost:5000

curl http://localhost:5000/hello

curl http://localhost:5000/error
```

---

# Run Using Docker

Build the image

```bash
docker build -t flask-jaeger-otel:v1 .
```

Run the container

```bash
docker run -d \
--name flask-jaeger-otel \
-p 5000:5000 \
-e OTEL_EXPORTER_OTLP_ENDPOINT=http://<JAEGER_HOST>:4318/v1/traces \
flask-jaeger-otel:v1
```

Example

```bash
docker run -d \
--name flask-jaeger-otel \
-p 5000:5000 \
-e OTEL_EXPORTER_OTLP_ENDPOINT=http://192.168.1.10:32221/v1/traces \
flask-jaeger-otel:v1
```

Verify

```bash
curl http://localhost:5000

curl http://localhost:5000/hello
```

---

# Push Image to Docker Hub

Tag the image

```bash
docker tag flask-jaeger-otel:v1 rootpromptnext/flask-jaeger-otel:v1
```

Push the image

```bash
docker push rootpromptnext/flask-jaeger-otel:v1
```

---

# Deploy on Kubernetes

Deploy the application

```bash
kubectl apply -f deployment.yaml
```

Verify

```bash
kubectl get pods -n observability

kubectl get svc -n observability
```

Application URL

```
http://<NODE-IP>:30501
```

Example

```bash
curl http://<NODE-IP>:30501

curl http://<NODE-IP>:30501/hello

curl http://<NODE-IP>:30501/error
```

---

# View Traces

Open the Jaeger UI

```
http://<NODE-IP>:30686
```

Select the service

```
flask-jaeger-otel
```

Click

```
Find Traces
```

Open any trace to view the generated spans.

---

# Cleanup

Docker

```bash
docker stop flask-jaeger-otel

docker rm flask-jaeger-otel
```

Kubernetes

```bash
kubectl delete -f deployment.yaml
```
