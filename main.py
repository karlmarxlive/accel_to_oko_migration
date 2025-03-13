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
ACCEL_API_URL = "https://api.accelonline.io/api"
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


def main():
    logger.info("Начало тестирования. Создаю контакт в Oko")
    oko_api = OkoAPI(OKO_API_URL, OKO_API_TOKEN)
    payload = {'name': 'Lana Raynor',
            'phones[][phone]': '568-371-6852',
            'emails[][email]': 'Bonita.Wuckert37@gmail.com',
            'tags[]': 'partnerships'}
    response = oko_api.create_contact(payload)
    logger.info("Контакт создан")
    logger.info(response)
    logger.info("Тестирование завершено")

if __name__ == "__main__":
    main()