import allure
import jsonschema
import pytest
import requests
from tests.store.schemas.store_schemas import STORE_SCHEMA, INVENTORY_SCHEMA

BASE_URL = "https://swagger.rv-school.ru/api/v3/"

#Шестой урок
@allure.feature("Store")
class TestStore:

    #Задание №6.1 (тест-кейс 42)
    @allure.title('Попытка размещения заказа')
    def test_placing_an_order(self):
        with allure.step('Подготовка данных для создания заказа'):
            payload = {
                "id": 1,
                "petId": 1,
                "quantity": 1,
                "status": "placed",
                "complete": True
            }
            response = requests.post(url=f'{BASE_URL}store/order', json=payload)

        with allure.step('Проверка статуса ответа и валидация JSON-схемы'):
            assert response.status_code == 200, 'Код ответа не совпал с ожидаемым'
            response_json = response.json()
            jsonschema.validate(response_json, STORE_SCHEMA)

    #Задание №6.2 (тест-кейс 43)
    @allure.title('Попытка найти информацию о заказе по ID')
    def test_find_order_id (self, create_order):
        with allure.step('Получение ID созданного заказа'):
            order_id= create_order["id"]

        with allure.step('Отправка запроса на получение информации по ID заказа'):
                response = requests.get(url=f'{BASE_URL}store/order/{order_id}')

        with allure.step('Проверка статуса ответа'):
                assert response.status_code == 200, 'Код ответа не совпал с ожидаемым'

    #Задание №6.3 (тест-кейс 44)
    @allure.title('Попытка удалить заказа по ID')
    def test_delete_order_id(self, create_order):
        with allure.step('Получение ID созданного заказа'):
            order_id = create_order["id"]

        with allure.step('Отправка запроса на удаление заказа по ID'):
            response = requests.delete(url=f'{BASE_URL}store/order/{order_id}')

        with allure.step('Проверка статуса ответа'):
            assert response.status_code == 200, 'Код ответа не совпал с ожидаемым'

        with allure.step('Отправка запроса на получение несуществующего заказа'):
            response = requests.get(url=f'{BASE_URL}store/order/{order_id}')
            assert response.status_code == 404, 'Код ответа не совпал с ожидаемым'

    #Задание №№6.4 (тест-кейс 45)

    @allure.title('Попытка найти информацию о заказе по ID')
    def test_find_noneexistent_order(self):
        with allure.step('Отправка запроса на получение информации по ID заказа'):
            response = requests.get(url=f'{BASE_URL}store/order/9999')

        with allure.step('Проверка статуса ответа'):
            assert response.status_code == 404, 'Код ответа не совпал с ожидаемым'

    #Задание №6.5 (тест-кейс 46)
    @allure.title('Попытка получения инвентаря магазина')
    def test_find_inventory(self):
        with allure.step('Отправка запроса на получение информации инвентаря магазина'):
            response = requests.get(url=f'{BASE_URL}store/inventory')
            inventory = response.json()

        with allure.step ('Проверка статуса ответа и формата данных'):
            assert response.status_code == 200, 'Код ответа не совпал с ожидаемым'
            assert isinstance(inventory, dict)
            jsonschema.validate(inventory, INVENTORY_SCHEMA)










