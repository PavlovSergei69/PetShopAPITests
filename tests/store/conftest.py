import pytest
import requests

BASE_URL = "https://swagger.rv-school.ru/api/v3/"

@pytest.fixture(scope="function")
def create_order():
    """Фикстура для создания заказа"""
    payload = {
        "id": 1,
        "petId": 1,
        "quantity": 1,
        "status": "placed",
        "complete": True
    }
    response = requests.post(url=f'{BASE_URL}store/order', json=payload)
    assert response.status_code == 200
    return response.json()
