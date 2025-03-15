import requests
import json
import time
from typing import Dict, List, Any, Optional
from logger_config import get_logger
from config import *
from apis import AccelAPI, OkoAPI

logger = get_logger()

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

    logger.info('Start test. Geting data from Accel')
    accel_api = AccelAPI(ACCEL_API_URL, ACCEL_API_TOKEN)
    response = accel_api.get_all_leads()
    logger.info('Request sent. Response:')
    logger.info(response)
    logger.info('Test cmpleted')

if __name__ == "__main__":
    main()