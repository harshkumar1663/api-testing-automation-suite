"""
HTTP client wrapper around the `requests` library.

Responsible for:
- Issuing HTTP requests
- Applying timeouts
- Basic error handling and logging

Author: Harsh Kumar
"""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional

import requests  # type: ignore

from .config import Config

logger = logging.getLogger(__name__)


class APIClientError(RuntimeError):
    """Raised when an HTTP request fails at a transport level."""


class HttpClient:
    """
    Thin wrapper over `requests` to centralise logging and error handling.
    """

    def __init__(self, config: Config) -> None:
        self.config = config

    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> requests.Response:
        """
        Perform a GET request to `base_url + path`.
        """
        url = self._build_url(path)
        logger.info("GET %s params=%s", url, params)
        try:
            headers = {"User-Agent": "API-Testing-Automation-Suite/1.0"}
            response = requests.get(url, params=params, timeout=self.config.timeout, headers=headers)
        except requests.RequestException as exc:  # network/connection errors
            logger.exception("GET request failed: %s", exc)
            raise APIClientError(str(exc)) from exc
        return response

    def post(self, path: str, json: Optional[Dict[str, Any]] = None) -> requests.Response:
        """
        Perform a POST request to `base_url + path`.
        """
        url = self._build_url(path)
        logger.info("POST %s json=%s", url, json)
        try:
            headers = {"User-Agent": "API-Testing-Automation-Suite/1.0"}
            response = requests.post(url, json=json, timeout=self.config.timeout, headers=headers)
        except requests.RequestException as exc:
            logger.exception("POST request failed: %s", exc)
            raise APIClientError(str(exc)) from exc
        return response

    def _build_url(self, path: str) -> str:
        """
        Compose full URL from base_url and path.
        """
        if path.startswith("http://") or path.startswith("https://"):
            return path
        # Ensure exactly one slash between base and path
        return f"{self.config.base_url.rstrip('/')}/{path.lstrip('/')}"
