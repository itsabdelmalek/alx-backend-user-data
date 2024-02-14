#!/usr/bin/env python3
"""
Basic Authentication module for the API
"""

from api.v1.auth.auth import Auth
from typing import TypeVar, List
from models.user import User
import base64
import binascii


class BasicAuth(Auth):
    """
    Class for handling basic authentication
    """

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
        Extract the Base64 part of the Authorization header for Basic Authn
        Returns:
            The Base64 part of the Authorization header or None.
        """
        if (authorization_header is None or
                not isinstance(authorization_header, str) or
                not authorization_header.strip().startswith("Basic")):
            return None

        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        Decode the Base64 string base64_authorization_header.
        Returns:
            The decoded value as a UTF8 string or None.
        """
        b64_auth_hdr = base64_authorization_header
        if b64_auth_hdr and isinstance(b64_auth_hdr, str):
            try:
                encode = b64_auth_hdr.encode('utf-8')
                base = base64.b64decode(encode)
                return base.decode('utf-8', errors='replace')
            except binascii.Error:
                return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
        Extract user email and password from the Base64 decoded value.
        Returns:
            Tuple containing user email and password or (None, None).
        """
        if (decoded_base64_authorization_header and
           isinstance(decoded_base64_authorization_header, str)):
            user_creds = decoded_base64_authorization_header.split(':', 1)
            return tuple(user_creds) if len(user_creds) == 2 else (None, None)
        return (None, None)

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):

        """
        Get the User instance based on email and password.
        Returns:
            User instance or None.
        """
        if not user_email or not user_pwd \
                or type(user_email) != str or type(user_pwd) != str:
            return None
        try:
            user = User.search({'email': user_email})
        except KeyError:
            return None
        if not user or not user[0].is_valid_password(user_pwd):
            return None
        return user[0]

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieve the User instance for a request.
        Returns:
            User instance or None.
        """
        header = self.authorization_header(request)
        b64_header = self.extract_base64_authorization_header(header)
        decoded = self.decode_base64_authorization_header(b64_header)
        user_creds = self.extract_user_credentials(decoded)
        return self.user_object_from_credentials(*user_creds)
