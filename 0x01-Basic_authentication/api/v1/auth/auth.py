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
        Check if authentication is required for the given path.
        Returns:
            True if authentication is required, False otherwise.
        """
        check = path
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path[-1] != "/":
            check += "/"
        if check in excluded_paths or path in excluded_paths:
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
