#!/usr/bin/env python3
"""
SessionDBAuth module for the API
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from api.v1.app import db


class SessionDBAuth(SessionExpAuth):
    """
    SessionDBAuth class
    """

    def create_session(self, user_id=None):
        """
        Creates and stores a new instance of UserSession
        """
        session_id = super().create_session(user_id)
        if session_id is not None:
            user_session = UserSession(user_id=user_id, session_id=session_id)
            db.add(user_session)
            db.commit()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Retrieves User ID from UserSession in the database based on session_id
        """
        if session_id is None:
            return None

        u_sess = db.query(UserSession).filter_by(session_id=session_id).first()

        if u_sess is None:
            return None

        return u_sess.user_id

    def destroy_session(self, request=None):
        """
        Destroys the UserSession based on the Session ID from the reques cookie
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        u_sess = db.query(UserSession).filter_by(session_id=session_id).first()

        if u_sess is None:
            return False

        db.delete(u_sess)
        db.commit()
        return True
