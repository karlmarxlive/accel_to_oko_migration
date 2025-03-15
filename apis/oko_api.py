import requests
from typing import Dict
from logger_config import get_logger

logger = get_logger()

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