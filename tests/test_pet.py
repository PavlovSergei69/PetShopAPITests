import allure
import jsonschema
#import requests необходим для формирования базы API-запросов
import requests
# импортируем схему с файла пет_схема. Не забывать про "." перед schemas
from .schemas.pet_schema import PET_SCHEMA

BASE_URL = 'http://5.181.109.28:9090/api/v3/'

@allure.feature("Pet")
class Testpet:

    #Первый урок
    @allure.title('Попытка удалить несуществующего питомца')
    def test_delete_noneexistent_pet(self):
        #step-шаг
        with allure.step('Отправка запроса на удаление несуществующего питомца'):
            responce = requests.delete(url=f'{BASE_URL}pet/9999')

        with allure.step('Проверка статуса ответа'):
            assert responce.status_code == 200, 'Код ответа не совпал с ожидаемым'
        with allure.step('Проверка текстового содержимого ответа'):
            assert responce.text == 'Pet deleted', 'Текст ошибки не совпал с ожидаемым'

    #Второй урок
    @allure.title('Попытка обновить несуществующего питомца')
    def test_update_noneexistent_pet(self):
        with allure.step('Отправка запроса на обновление несуществующего питомца'):
            payload = {
                "id": 9999,
                "name": "Non-existent Pet",
                "status": "available"
            }
            responce = requests.put(url=f'{BASE_URL}pet/', json = payload)

        with allure.step('Проверка статуса ответа'):
            assert responce.status_code == 404, 'Код ответа не совпал с ожидаемым'
        with allure.step('Проверка текстового содержимого ответа'):
            assert responce.text == 'Pet not found', 'Текст ошибки не совпал с ожидаемым'

    #Задание №2
    @allure.title('Попытка найти несуществующего питомца')
    def test_find_noneexistent_pet(self):
        with allure.step('Отправка запроса на получение несуществующего питомца'):
            responce = requests.get(url=f'{BASE_URL}pet/9999')

        with allure.step('Проверка статуса ответа'):
            assert responce.status_code == 404, 'Код ответа не совпал с ожидаемым'
        with allure.step('Проверка текстового содержимого ответа'):
            assert responce.text == 'Pet not found', 'Текст ошибки не совпал с ожидаемым'

    #Третий урок
    @allure.title('Добавление нового питомца')
    def test_add_pet(self):
        with allure.step('Подготовка данных для создания питомца'):
            payload = {
                "id": 1,
                "name": "Buddy",
                "status": "available"
            }
            responce = requests.post(url=f'{BASE_URL}pet/', json=payload)
            responce_json = responce.json()

        with allure.step('Проверка статуса ответа и валидация JSON-схемы'):
            assert responce.status_code == 200, 'Код ответа не совпал с ожидаемым'
            jsonschema.validate(responce_json, PET_SCHEMA)

        with allure.step('Проверка параметров питомца в ответе'):
            assert responce_json["id"] == payload["id"], 'id питомца не совпадает'
            assert responce_json["name"] == payload["name"], 'имя питомца не совпадает'
            assert responce_json["status"] == payload["status"], 'статус питомца не совпадает'

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
            responce = requests.post(url=f'{BASE_URL}pet/', json=payload)
            responce_json = responce.json()

        with allure.step('Проверка статуса ответа и валидация JSON-схемы'):
            assert responce.status_code == 200, 'Код ответа не совпал с ожидаемым'
            jsonschema.validate(responce_json, PET_SCHEMA)

        with allure.step('Проверка параметров питомца в ответе'):
            assert responce_json["id"] == payload["id"], 'id питомца не совпадает'
            assert responce_json["name"] == payload["name"], 'имя питомца не совпадает'
            assert responce_json["status"] == payload["status"], 'статус питомца не совпадает'