import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class BaseClient:
    """Base HTTP client with retry, timeout and JSON parsing."""

    def __init__(
        self,
        base_url: str,
        timeout: int = 30,
        retries: int = 3,
        backoff_factor: float = 0.5,
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

        retry_strategy = Retry(
            total=retries,
            backoff_factor=backoff_factor,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"],
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)

        self.session = requests.Session()
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def get(self, endpoint: str, params: dict | None = None) -> dict:
        """
        Send GET request and return JSON response.
        """

        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        response = self.session.get(
            url,
            params=params,
            timeout=self.timeout,
        )

        response.raise_for_status()

        return response.json()