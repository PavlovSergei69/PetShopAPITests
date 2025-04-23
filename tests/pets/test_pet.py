import allure
import jsonschema
import pytest
#import requests необходим для формирования базы API-запросов
import requests
# импортируем схему с файла пет_схема. Не забывать про "." перед schemas
from .schemas.pet_schema import PET_SCHEMA

BASE_URL = "https://swagger.rv-school.ru/api/v3/"

@allure.feature("Pet")
class Testpet:

    #Первый урок
    @allure.title('Попытка удалить несуществующего питомца')
    def test_delete_noneexistent_pet(self):
        #step-шаг
        with allure.step('Отправка запроса на удаление несуществующего питомца'):
            response = requests.delete(url=f'{BASE_URL}pet/9999')

        with allure.step('Проверка статуса ответа'):
            assert response.status_code == 200, 'Код ответа не совпал с ожидаемым'
        with allure.step('Проверка текстового содержимого ответа'):
            assert response.text == 'Pet deleted', 'Текст ошибки не совпал с ожидаемым'

    #Второй урок
    @allure.title('Попытка обновить несуществующего питомца')
    def test_update_noneexistent_pet(self):
        with allure.step('Отправка запроса на обновление несуществующего питомца'):
            payload = {
                "id": 9999,
                "name": "Non-existent Pet",
                "status": "available"
            }
            response = requests.put(url=f'{BASE_URL}pet', json = payload)

        with allure.step('Проверка статуса ответа'):
            assert response.status_code == 404, 'Код ответа не совпал с ожидаемым'
        with allure.step('Проверка текстового содержимого ответа'):
            assert response.text == 'Pet not found', 'Текст ошибки не совпал с ожидаемым'

    #Задание №2
    @allure.title('Попытка найти несуществующего питомца')
    def test_find_noneexistent_pet(self):
        with allure.step('Отправка запроса на получение несуществующего питомца'):
            response = requests.get(url=f'{BASE_URL}pet/9999')

        with allure.step('Проверка статуса ответа'):
            assert response.status_code == 404, 'Код ответа не совпал с ожидаемым'
        with allure.step('Проверка текстового содержимого ответа'):
            assert response.text == 'Pet not found', 'Текст ошибки не совпал с ожидаемым'

    #Третий урок
    @allure.title('Добавление нового питомца')
    def test_add_pet(self):
        with allure.step('Подготовка данных для создания питомца'):
            payload = {
                "id": 1,
                "name": "Buddy",
                "status": "available"
            }
            response = requests.post(url=f'{BASE_URL}pet', json=payload)
            response_json = response.json()

        with allure.step('Проверка статуса ответа и валидация JSON-схемы'):
            assert response.status_code == 200, 'Код ответа не совпал с ожидаемым'
            jsonschema.validate(response_json, PET_SCHEMA)

        with allure.step('Проверка параметров питомца в ответе'):
            assert response_json["id"] == payload["id"], 'id питомца не совпадает'
            assert response_json["name"] == payload["name"], 'имя питомца не совпадает'
            assert response_json["status"] == payload["status"], 'статус питомца не совпадает'

    #Задание №3
    @allure.title('Добавление нового питомца с полными данными')
    def test_add_pet_with_full_data(self):
        with allure.step('Подготовка данных для создания питомца c полными данными'):
            payload = {
                "id": 10,
                "name": "doggie",
                "category": {
                    "id": 1,
                    "name": "Dogs"
                },
                "photoUrls": ["string"],
                "tags": [
                     {
                        "id": 0,
                        "name": "string"
                     }
                ],
                "status": "available"
            }
            response = requests.post(url=f'{BASE_URL}pet', json=payload)
            response_json = response.json()

        with allure.step('Проверка статуса ответа и валидация JSON-схемы'):
            assert response.status_code == 200, 'Код ответа не совпал с ожидаемым'
            jsonschema.validate(response_json, PET_SCHEMA)

        with allure.step('Проверка параметров питомца в ответе'):
            assert response_json["id"] == payload["id"], 'id питомца не совпадает'
            assert response_json["name"] == payload["name"], 'имя питомца не совпадает'
            assert response_json["status"] == payload["status"], 'статус питомца не совпадает'

    #Четвертый урок
    @allure.title('Получение информации о питомце по ID')
    #Фикстура вписывается в сам тест (create_pet)
    def test_get_pet_by_id(self,create_pet):
        with allure.step('Получение ID создания питомца'):
            pet_id= create_pet["id"]

        with allure.step('Отправка запроса на получение информации о питомце по ID'):
            response = requests.get(f'{BASE_URL}pet/{pet_id}')

        with allure.step('Проверка статуса ответа и данных питомца'):
            assert response.status_code == 200, 'Код ответа не совпал с ожидаемым'
            assert response.json()["id"] == pet_id

    #Задание №4.1
    @allure.title('Попытка обновить информацию о питомце')
    def test_update_pet(self,create_pet):
        with allure.step('Получение ID созданного питомца'):
            pet_id = create_pet["id"]

        with allure.step('Отправка запроса на обновление питомца'):
            payload = {
                "id": pet_id,
                "name": "Buddy Updated",
                "status": "sold"
            }
            response = requests.put(url=f'{BASE_URL}pet', json=payload)
            response_json = response.json()

        with allure.step('Проверка статуса ответа и данных питомца'):
            assert response.status_code == 200, 'Код ответа не совпал с ожидаемым'

            #Дополнительные проверки изменения данных
            assert response_json["id"] == payload["id"], 'id питомца не совпадает'
            assert response_json["name"] == payload["name"], 'имя питомца не совпадает'
            assert response_json["status"] == payload["status"], 'статус питомца не совпадает'

    #Задание №4.2
    @allure.title('Попытка удалить питомца')
    def test_delete_pet(self,create_pet):
        with allure.step('Получение ID созданного питомца'):
            pet_id= create_pet["id"]

        with allure.step('Отправка запроса на удаление питомце'):
                response = requests.delete(url=f'{BASE_URL}pet/{pet_id}')
        with allure.step('Проверка статуса ответа'):
                assert response.status_code == 200, 'Код ответа не совпал с ожидаемым'

        with allure.step('Отправка запроса на получение несуществующего питомца'):
            response = requests.get(url=f'{BASE_URL}pet/{pet_id}')
            assert response.status_code == 404, 'Код ответа не совпал с ожидаемым'

    #Пятый урок
    @allure.title('Получение списка питомцев по статусу')
    @pytest.mark.parametrize(
        "status, expected_status_code",
        [
            ("available",200),
            ("pending",200),
    #Задание №5
            ("sold",200),
            ("reserved",400),
            ("",400)
        ]
    )
    def test_get_pets_by_status(self,status,expected_status_code):
        with allure.step(f'Отправка запроса на получение питомцев по статусу {status}'):
            response = requests.get(url=f'{BASE_URL}pet/findByStatus', params={"status": status})

        with allure.step('Проверка статуса ответа'):
                assert response.status_code == expected_status_code, 'Код ответа не совпал с ожидаемым'
                assert isinstance(response.json(),list)


