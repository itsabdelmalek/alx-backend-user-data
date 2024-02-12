#!/usr/bin/env python3
"""
Authentication module for the API
"""

from tabnanny import check
from flask import request
from typing import List, TypeVar
User = TypeVar('User')


class Auth:
    """
    Class for managing API authentication.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Check if authentication is required for the given path
        Returns:
            True if authentication is required, False otherwise.
        """
        if path is None or not excluded_paths:
            return True
        for excluded_path in excluded_paths:
            if path.startswith(excluded_path.rstrip('*')):
                return False
            return True

    def authorization_header(self, request=None) -> str:
        """
        Get the authorization header from the request
        Returns:
            The authorization header value or None
        """
        if request is None:
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> User:
        """
        Get the current authenticated user.
        Returns:
            The current authenticated user or None.
        """
        return None
