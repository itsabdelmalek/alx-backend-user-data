#!/usr/bin/env python3
"""
Session ExpAuthentication module for the API
"""

from datetime import datetime, timedelta
from api.v1.auth.session_auth import SessionAuth
import os


class SessionExpAuth(SessionAuth):
    """
    Session expiration auth class
    """

    def __init__(self):
        """
        Constructor method
        """
        super().__init__()
        # Assign session_duration from environment variable
        self.session_duration = int(os.getenv("SESSION_DURATION", 0))

    def create_session(self, user_id=None):
        """
        Creates a Session ID with expiration date
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        # Create a session dictionary
        session_dict = {
            "user_id": user_id,
            "created_at": datetime.now()
        }

        # Store the session dictionary in user_id_by_session_id
        self.user_id_by_session_id[session_id] = session_dict

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Retrieves User ID from Session ID with expiration check
        """
        if session_id is None or session_id not in self.user_id_by_session_id:
            return None

        session_dict = self.user_id_by_session_id[session_id]

        if self.session_duration <= 0:
            return session_dict.get("user_id")

        created_at = session_dict.get("created_at")

        if created_at is None:
            return None

        expiration_time = created_at + timedelta(seconds=self.session_duration)

        if expiration_time < datetime.now():
            return None

        return session_dict.get("user_id")
