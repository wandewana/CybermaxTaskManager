import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_task(async_client: AsyncClient, auth_token: str):
    """Test creating a new task as an authenticated user."""
    headers = {"Authorization": f"Bearer {auth_token}"}
    task_data = {
        "title": "Test Task from Pytest",
        "description": "This is a test task."
    }
    response = await async_client.post("/tasks/", headers=headers, json=task_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == task_data["title"]
    assert data["description"] == task_data["description"]
    assert "id" in data
