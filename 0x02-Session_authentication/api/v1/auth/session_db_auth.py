#!/usr/bin/env python3
"""
SessionDBAuth module for the API
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """
    SessionDBAuth class
    """

    def __init__(self):
        """
        Initialize SessionDBAuth
        """
        super().__init__()
        self.db = []

    def create_session(self, user_id=None):
        """
        Create a Session ID and store it in the database.
        """
        session_id = super().create_session(user_id)
        if session_id:
            user_session = UserSession(user_id=user_id, session_id=session_id)
            self.db.append(user_session)
            return session_id
        return None

    def user_id_for_session_id(self, session_id=None):
        """
        Return the User ID by requesting UserSession in the database.
        """
        if not session_id:
            return None

        for user_session in self.db:
            if user_session.session_id == session_id:
                return super().user_id_for_session_id(session_id)

        return None

    def destroy_session(self, request=None):
        """
        Destroy the UserSession based on the Session ID from the request cookie
        """
        session_id = self.session_cookie(request)
        if not session_id:
            return False

        for user_session in self.db:
            if user_session.session_id == session_id:
                self.db.remove(user_session)
                return super().destroy_session(request)

        return False
