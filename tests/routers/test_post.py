import pytest
from httpx import AsyncClient


def create_post(body: str, async_client: AsyncClient) -> dict:
    response = await async_client.post("/posts", json={"body": body})
    return response.json()


@pytest.fixture()
async def created_post(async_client: AsyncClient):
    return create_post("Hello world", async_client)
