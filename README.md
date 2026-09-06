

# Distributed Systems Lab

A hands-on project for learning distributed systems by building a small multi-server backend architecture with Python.

## Current Features

- FastAPI backend application
- Multiple backend server instances
- Load balancing
- Health checks
- Basic fault tolerance
- Request timeouts
- Async HTTP communication with `httpx`

## Architecture

```text
Client
  ↓
Load Balancer :8080
  ↓
┌──────────┬──────────┬──────────┐
│ Server 1 │ Server 2 │ Server 3 │
│  :8001   │  :8002   │  :8003   │
└──────────┴──────────┴──────────┘
````

Each backend runs the same FastAPI application as a separate Uvicorn process.

## Backend Endpoints

```text
GET /
GET /health
```

`/health` is used by the load balancer to determine which backend servers are available.

## Run

Start the backend servers:

```powershell
$env:SERVER_ID="server-1"
uv run uvicorn backend.app:app --port 8001
```

```powershell
$env:SERVER_ID="server-2"
uv run uvicorn backend.app:app --port 8002
```

```powershell
$env:SERVER_ID="server-3"
uv run uvicorn backend.app:app --port 8003
```

Start the load balancer:

```powershell
uv run uvicorn load_balancer.app:app --port 8080
```

Then visit:

```text
http://127.0.0.1:8080/
```

## Concepts Learned

* Client-server communication
* HTTP and APIs
* Server processes
* Horizontal scaling
* Load balancing
* Health checks
* Fault tolerance
* Timeouts
* Async communication
