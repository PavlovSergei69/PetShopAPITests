import allure
#import requests необходим для формирования базы API-запросов
import requests

BASE_URL = 'http://5.181.109.28:9090/api/v3/'

@allure.feature("Pet")
class Testpet:
    @allure.title('Попытка удалить несуществующего питомца')
    def test_delete_noneexistent_pet(self):
        #step-шаг
        with allure.step('Отправка запроса на удаление несуществующего питомца'):
            responce = requests.delete(url=f'{BASE_URL}pet/9999')

        with allure.step('Проверка статуса ответа'):
            assert responce.status_code == 200, 'Код ответа не совпал с ожидаемым'
        with allure.step('Проверка текстового содержимого ответа'):
            assert responce.text == 'Pet deleted', 'Текст ошибки не совпал с ожидаемым'

