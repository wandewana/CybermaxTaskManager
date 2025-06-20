import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_register_user(async_client: AsyncClient):
    """
    Test user registration endpoint.
    """
    response = await async_client.post("/auth/register", json={
        "email": "newuser@example.com",
        "password": "newpassword123"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert "id" in data
    assert "hashed_password" not in data

@pytest.mark.asyncio
async def test_login_success(async_client: AsyncClient, test_user):
    """
    Test successful login with a pre-existing user.
    """
    response = await async_client.post("/auth/login", data={
        "username": test_user.email,
        "password": "password"  # The password for the fixture user
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_login_failure(async_client: AsyncClient):
    """
    Test login with incorrect credentials.
    """
    response = await async_client.post("/auth/login", data={
        "username": "wronguser@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"

@pytest.mark.asyncio
async def test_read_current_user(async_client: AsyncClient, auth_token: str):
    """
    Test fetching the current user with a valid token.
    """
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = await async_client.get("/users/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "testuser@example.com"  # Email from the fixture
