import requests
from src.utils import user_agent


class HTTPClient:
    @staticmethod
    def fetch_html_page(link: str) -> str | None:
        response = HTTPClient.request(link)
        if not response:
            return None
        return response.text

    @staticmethod
    def request(url: str, timeout: int = 10) -> requests.Response | None:
        try:
            response = requests.get(url=url,
                                    headers={'User-Agent': user_agent()},
                                    timeout=timeout)
        except Exception as e:
            print(f"Couldn't connect to {url}, {e}")
            return None

        if response.status_code != 200:
            print(f'Bad status code : {response.status_code}, {url}')
            return None

        return response
