import requests


class ServiceApiError(Exception):
    def __init__(self, message, status_code):
        self.message = message
        self.status_code = status_code


def fetch_data(url, timeout=5) -> dict:
    try:
        response = requests.get(url, timeout=timeout)
        return response.json()
    except requests.RequestException as e:
        raise ServiceApiError(
            message=e,
            status_code=500,
        )
