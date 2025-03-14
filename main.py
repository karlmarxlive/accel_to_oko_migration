import requests
import json
import time
import logging
from typing import Dict, List, Any, Optional
import os
from datetime import datetime

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f"migration_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Конфигурация API
ACCEL_API_URL = "https://api.accelonline.io/api/v1"
OKO_API_URL = "https://api.okocrm.com/v2"
ACCEL_API_TOKEN = os.environ.get("ACCEL_API_TOKEN")
OKO_API_TOKEN = os.environ.get("OKO_API_TOKEN")

# Классы для работы с API
class OkoAPI:
    def __init__(self, base_url, token):
        self.token = token
        self.base_url = base_url
        self.headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.token}"
        }

    def create_contact(self, contact_data: Dict) -> Dict:
        endpoint = '/contacts/'
        return self._make_request('POST', endpoint, data=contact_data)
    
    def _make_request(self, method, endpoint: str, params: Dict = None, data: Dict = None) -> dict:
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                params=params,
                data=data
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error making request: {e}")
            if hasattr(e, 'response') and hasattr(e.response, 'text'):
                logger.error(f"Response text: {e.response.text}")
            return {}

class AccelAPI:
    def __init__(self, base_url, token):
        self.token = token
        self.base_url = base_url
        self.headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.token}"
        }

    def get_all_leads(self, fields: list = None) -> Dict:
        """
        Получение списка всех лидов (контактов) из Accel
        
        Args:
            page: Номер страницы (начиная с 1)
            page_size: Количество записей на странице
            fields: Список полей, которые нужно получить (по умолчанию id, email, firstName)
        
        Returns:
            Dict: Словарь с данными о лидах
        """

        endpoint = '/crm/lead'

        if fields is None:
            fields = ['id', 'firstName', 'lastName', 'email', 'phone']

        fields_str = '{' + ', '.join(fields) + '}'

        params = {
            #'page': page,
            #'pageSize': page_size,
            'fields': fields_str
        }

        return self._make_request("GET", endpoint, params=params)
    
    def _make_request(self, method: str, endpoint: str, params: Dict = None, data: Dict = None) -> Dict:
        url = f'{self.base_url}{endpoint}'

        if params and 'fields' in params and isinstance(params['fields'], str):
            fields = params['fields']
            if not (fields.startswith('{') and fields.endswith('}')):
                params['fields'] = '{' + fields + '}'

        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                params=params,
                json=data
            )

            logger.debug(f"Request URL: {response.url}")
            logger.debug(f"Request headers: {self.headers}")
            logger.debug(f"Request params: {params}")
            logger.debug(f"Request data: {data}")

            response.raise_for_status()

            result = response.json()

            if not result.get('success', False):
                error_messages = [error.get('message', 'Unknown error') for error in result.get('errors', [])]
                logger.error(f"API returned error: {', '.join(error_messages)}")
            
            return result
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка при запросе к Accel API: {e}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    logger.error(f"Ответ сервера: {error_data}")
                except ValueError:
                    logger.error(f"Ответ сервера (не JSON): {e.response.text}")
                logger.error(f"Статус код: {e.response.status_code}")
            return {"success": False, "errors": [{"message": str(e)}], "body": None}
        
        except ValueError as e:
            logger.error(f"Ошибка при парсинге JSON: {e}")
            logger.error(f"Ответ сервера: {response.text}")
            return {"success": False, "errors": [{"message": "Invalid JSON response"}], "body": None}


def main():
    # logger.info("Начало тестирования. Создаю контакт в Oko")
    # oko_api = OkoAPI(OKO_API_URL, OKO_API_TOKEN)
    # payload = {'name': 'Lana Raynor',
    #         'phones[][phone]': '568-371-6852',
    #         'emails[][email]': 'Bonita.Wuckert37@gmail.com',
    #         'tags[]': 'partnerships'}
    # response = oko_api.create_contact(payload)
    # logger.info("Контакт создан")
    # logger.info(response)
    # logger.info("Тестирование завершено")

    logger.info('Начало тестирования. Получаю данные из Акселя')
    accel_api = AccelAPI(ACCEL_API_URL, ACCEL_API_TOKEN)
    response = accel_api.get_all_leads()
    logger.info('Запрос отправлен. Ответ:')
    logger.info(response)
    logger.info('Тестирование завершено')

if __name__ == "__main__":
    main()