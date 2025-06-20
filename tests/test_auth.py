import pytest

# Note: These tests will fail if run against a live database
# that already contains the test user. A separate test database
# or mocking is needed for robust testing.

@pytest.mark.asyncio
async def test_login_success(async_client):
    # First, register a user to ensure the user exists
    await async_client.post("/auth/register", json={
        "email": "valid@example.com", "password": "abc123"
    })
    # Then, attempt to log in with the correct credentials
    response = await async_client.post("/auth/login", json={
        "email": "valid@example.com", "password": "abc123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

@pytest.mark.asyncio
async def test_login_failure(async_client):
    # Attempt to log in with credentials that do not exist
    response = await async_client.post("/auth/login", json={
        "email": "nope@example.com", "password": "wrong"
    })
    assert response.status_code == 401
