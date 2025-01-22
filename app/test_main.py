import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_create_contact():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/contacts/",
            json={
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
                "phone": "123456789",
                "birthday": "1990-01-01",
                "additional_info": "Test contact"
            },
        )
    assert response.status_code == 200
    assert response.json()["first_name"] == "John"
