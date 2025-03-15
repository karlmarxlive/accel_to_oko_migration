import requests
from typing import Dict
from logger_config import get_logger

logger = get_logger()

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
            logger.error(f"Error while accessing Accel API: {e}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    logger.error(f"Server response: {error_data}")
                except ValueError:
                    logger.error(f"Server response (not a JSON): {e.response.text}")
                logger.error(f"Code status: {e.response.status_code}")
            return {"success": False, "errors": [{"message": str(e)}], "body": None}
        
        except ValueError as e:
            logger.error(f"Error while parsing JSON: {e}")
            logger.error(f"Server response: {response.text}")
            return {"success": False, "errors": [{"message": "Invalid JSON response"}], "body": None}
