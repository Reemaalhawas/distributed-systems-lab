from fastapi import FastAPI
import httpx
import itertools

app = FastAPI()

BACKEND_SERVERS = [
    "http://127.0.0.1:8001",
    "http://127.0.0.1:8002",
    "http://127.0.0.1:8003",
]


async def get_healthy_servers():
    healthy_servers = []

    async with httpx.AsyncClient() as client:
        for server in BACKEND_SERVERS:
            try:
                response = await client.get(
                    f"{server}/health",
                    timeout=1.0
                )

                if response.status_code == 200:
                    healthy_servers.append(server)

            except httpx.RequestError:
                pass

    return healthy_servers


@app.get("/")
async def load_balance():
    healthy_servers = await get_healthy_servers()

    if not healthy_servers:
        return {
            "error": "No healthy backend servers available"
        }

    server_cycle = itertools.cycle(healthy_servers)
    backend = next(server_cycle)

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{backend}/")

    return {
        "forwarded_to": backend,
        "backend_response": response.json()
    }