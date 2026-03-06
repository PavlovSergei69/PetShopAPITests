import pytest #response_json - переменная, response.json() - функция
import requests

BASE_URL = "http://5.181.109.28:9090/api/v3/"

@pytest.fixture(scope="function") #scope время действия фикстуры
def create_pet():
    """Фикстура для создания питомца"""
    payload = {
        "id": 1,
        "name": "Buddy",
        "status": "available"
    }
    response = requests.post(url=f'{BASE_URL}pet', json=payload)
    assert response.status_code == 200
    return response.json()