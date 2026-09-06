# Distributed Systems Lab

A hands-on learning project for understanding the core ideas behind distributed systems by building a small multi-server architecture from scratch.

The project currently includes:

- A FastAPI backend application
- Multiple backend server instances running on different ports
- A simple load balancer
- Backend health checks
- Request timeouts

## Current Architecture

```text
Client
  |
  v
Load Balancer :8080
  |
  +-------------------+-------------------+
  |                   |                   |
  v                   v                   v
Server 1            Server 2            Server 3
:8001               :8002               :8003
```

All backend instances run the same FastAPI application but are started as separate Uvicorn processes.

## Backend Application

The backend application is defined in:

```text
backend/app.py
```

It exposes two GET endpoints:

### `GET /`

Returns a simple response identifying the backend server that handled the request.

Example:

```json
{
  "message": "Hello from backend server",
  "server_id": "server-1"
}
```

### `GET /health`

Used by the load balancer to check whether a backend server is available.

Example:

```json
{
  "status": "healthy",
  "server_id": "server-1"
}
```

The server ID is read from an environment variable so the same application code can be run as multiple independent server instances.

## Running Multiple Backend Instances

On PowerShell, start three backend servers in separate terminals.

### Server 1

```powershell
$env:SERVER_ID="server-1"
uv run uvicorn backend.app:app --port 8001
```

### Server 2

```powershell
$env:SERVER_ID="server-2"
uv run uvicorn backend.app:app --port 8002
```

### Server 3

```powershell
$env:SERVER_ID="server-3"
uv run uvicorn backend.app:app --port 8003
```

Each process runs the same FastAPI application independently on a different port.

## Load Balancer

The load balancer is defined in:

```text
load_balancer/app.py
```

It maintains a list of backend server addresses and performs two main tasks:

1. Checks which backend servers are healthy.
2. Forwards the incoming request to one of the healthy backends.

Run the load balancer with:

```powershell
uv run uvicorn load_balancer.app:app --port 8080
```

Then open:

```text
http://127.0.0.1:8080/
```

The load balancer sends an HTTP request to a backend and returns both the selected backend address and its response.

## Health Checks

Before forwarding traffic, the load balancer sends:

```text
GET /health
```

to each configured backend server.

A backend is considered healthy when it responds successfully with HTTP status `200`.

The health-check request has a one-second timeout:

```python
timeout=1.0
```

If a server cannot be reached within that time, it is excluded from the healthy server list.

This introduces a basic form of fault tolerance: one backend can become unavailable while the remaining healthy backends continue serving requests.

## Request Timeout

The actual request forwarded from the load balancer to a backend also has a timeout:

```python
timeout=2.0
```

This prevents the load balancer from waiting indefinitely for a backend response.

Health-check timeouts and request timeouts solve different problems:

- Health-check timeout: determines whether a backend should be considered available.
- Request timeout: limits how long the system waits for the actual request to complete.

## Concepts Covered So Far

This project currently demonstrates:

- Client-server communication
- HTTP requests and responses
- FastAPI routes and endpoints
- Uvicorn server processes
- IP addresses and ports
- Multiple instances of the same service
- Horizontal scaling
- Load balancing
- Health checks
- Basic fault tolerance
- Timeouts
- Asynchronous HTTP requests with `httpx`

## Project Structure

```text
distributed-systems-lab/
|
+-- backend/
|   +-- app.py
|
+-- load_balancer/
|   +-- app.py
|
+-- README.md
+-- pyproject.toml
```

## Learning Goal

The goal of this repository is to progressively build a small distributed system and understand why each component exists.

Future iterations may explore concepts such as service discovery, caching, queues and workers, shared databases, replication, consistency, observability, containerization, and other distributed-systems patterns.

This repository is intentionally built incrementally so that each new feature introduces a specific systems-engineering concept.