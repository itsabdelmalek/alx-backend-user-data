#!/usr/bin/env python3
"""
Authentication module for the API
"""

from tabnanny import check
from flask import request
from typing import List, TypeVar
from fnmatch import fnmatch
import os
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
        if not path or not excluded_paths:
            return True
        if path[-1] != '/':
            path += '/'
        return not [n for n in excluded_paths if fnmatch(path, n)]

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

    def session_cookie(self, request=None) -> str:
        """
        Get the value of the session cookie from the request.
        Returns:
            The session cookie value or None.
        """
        if request is None:
            return None
        session_name = os.getenv("SESSION_NAME", "_my_session_id")
        return request.cookies.get(session_name)
