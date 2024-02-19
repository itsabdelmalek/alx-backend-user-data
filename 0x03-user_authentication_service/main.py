#!/usr/bin/env python3
"""
Main file
"""
import requests

BASE_URL = "http://127.0.0.1:5000"


def register_user(email: str, password: str) -> None:
    url = f"{BASE_URL}/users"
    data = {"email": email, "password": password}
    response = requests.post(url, data=data)

    if response.status_code != 201:
        print(f"Failed to register user: {response.text}")


def log_in_wrong_password(email: str, password: str) -> None:
    url = f"{BASE_URL}/sessions"
    data = {"email": email, "password": password}
    response = requests.post(url, data=data)
    assert response.status_code == 401, "Incorrect password should return 401"


def log_in(email: str, password: str) -> str:
    url = f"{BASE_URL}/sessions"
    data = {"email": email, "password": password}
    response = requests.post(url, data=data)

    try:
        return response.json().get("session_id", "Session ID not found.")
    except ValueError:
        print(f"Failed to log in: {response.text}")


def profile_unlogged() -> None:
    url = f"{BASE_URL}/profile"
    response = requests.get(url)
    assert response.status_code == 403, "Profile request return 403"


def profile_logged(session_id: str) -> None:
    url = f"{BASE_URL}/profile"
    cookies = {"session_id": session_id}
    response = requests.get(url, cookies=cookies)
    assert response.status_code == 200, f"Failed to get : {response.text}"


def log_out(session_id: str) -> None:
    url = f"{BASE_URL}/sessions"
    cookies = {"session_id": session_id}
    response = requests.delete(url, cookies=cookies)
    assert response.status_code == 200, f"Failed to log out: {response.text}"


def reset_password_token(email: str) -> str:
    url = f"{BASE_URL}/reset_password"
    data = {"email": email}
    response = requests.post(url, data=data)
    assert response.status_code == 200, f"Failed to get token: {response.text}"
    return response.json()["reset_token"]


def update_password(email: str, reset_tkn: str, new_pswd: str) -> None:
    url = f"{BASE_URL}/reset_password"
    data = {"email": email, "reset_token": reset_tkn, "new_password": new_pswd}
    response = requests.put(url, data=data)
    assert response.status_code == 200, f"Failed to update : {response.text}"


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"

if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
