#!/usr/bin/env python3
"""
Session Authentication module for the API
"""

from uuid import uuid4
from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    """
    Class for handling session authentication
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        creates a Session ID for a user_id
        """
        if not user_id or type(user_id) != str:
            return None
        session_id = str(uuid4())
        SessionAuth.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        returns a User ID based on a Session ID
        """
        if not session_id or type(session_id) != str:
            return None
        return SessionAuth.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        Returns a User instance based on a cookie value
        """
        if not request:
            return None

        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)

        if not user_id:
            return None

        return User.get(user_id)

    def destroy_session(self, request=None):
        """
        Deletes the user session / logout
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if not session_id:
            return False

        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return False

        del SessionAuth.user_id_by_session_id[session_id]
        return True
