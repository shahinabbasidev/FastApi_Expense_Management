
import pytest


def test_register_success(anon_client):
    payload = {
        "first_name": "shahin",
        "last_name": "abbasi",
        "username": "shahin_ab",
        "password": "shahin123456",
    }
    response = anon_client.post("/users/register", json=payload)
    assert response.status_code == 201
    json = response.json()
    assert "user_id" in json
    assert "detail" in json


def test_register_conflict(anon_client):
    # registering the same user twice should produce a 409
    payload = {
        "first_name": "shahin",
        "last_name": "abbassi",
        "username": "shahin_ab",
        "password": "shahin123456",
    }
    anon_client.post("/users/register", json=payload)
    resp2 = anon_client.post("/users/register", json=payload)
    assert resp2.status_code == 409


def test_login_not_found(anon_client):
    payload = {"username": "no_such_user", "password": "whatever"}
    response = anon_client.post("/users/login", json=payload)
    assert response.status_code == 404


def test_login_wrong_password(anon_client):
    # rely on deterministic user from conftest
    payload = {"username": "testuser", "password": "wrongpass"}
    response = anon_client.post("/users/login", json=payload)
    assert response.status_code == 401


def test_login_success_sets_cookies(anon_client):
    payload = {"username": "testuser", "password": "testpass"}
    response = anon_client.post("/users/login", json=payload)
    assert response.status_code == 200
    # cookies should be set on the client instance
    assert "access_token" in response.cookies
    assert "refresh_token" in response.cookies


def test_refresh_token_missing(anon_client):
    response = anon_client.post("/users/refresh-token")
    assert response.status_code == 404


def test_refresh_token_success(anon_client):
    # perform login first to obtain cookies
    login = anon_client.post("/users/login", json={"username": "testuser", "password": "testpass"})
    assert login.status_code == 200
    # now cookies are available on anon_client
    response = anon_client.post("/users/refresh-token")
    assert response.status_code == 200
    assert "access_token" in response.cookies


def test_logout_clears_cookies(anon_client):
    # login to set cookies
    anon_client.post("/users/login", json={"username": "testuser", "password": "testpass"})
    response = anon_client.post("/users/logout")
    assert response.status_code == 200
    # cookies should be removed on the client side
    assert response.cookies.get("access_token") is None
    assert response.cookies.get("refresh_token") is None


def test_update_user_requires_auth(anon_client):
    payload = {"first_name": "New", "last_name": "Name", "username": "irrelevant", "password": "irrelevant"}
    resp = anon_client.put("/users/user-update", json=payload)
    assert resp.status_code == 401


def test_update_user_success(auth_client):
    payload = {"first_name": "Updated", "last_name": "User", "username": "shouldnotchange", "password": "newpass123"}
    resp = auth_client.put("/users/user-update", json=payload)
    assert resp.status_code == 200
    body = resp.json()
    assert body["user"]["first_name"] == "Updated"
    assert body["user"]["last_name"] == "User"
