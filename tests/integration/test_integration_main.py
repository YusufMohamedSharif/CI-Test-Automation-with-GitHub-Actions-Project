import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
import pytest
from fastapi.testclient import TestClient
from app.main import app, usersList, all_transactions

client = TestClient(app)
# from httpx import WSGITransport
# client = TestClient(app, transport=WSGITransport(app=app))

def test_get_signup_form():
    response = client.get("/")
    assert response.status_code == 200
    # Check for a unique string from the real HTML file
    assert "Peer to Peer transactions" in response.text

def test_post_signup():
    data = {"name": "TestUser", "email": "testuser@example.com", "password": "testpass"}
    response = client.post("/signup", data=data)
    assert response.status_code == 200
    assert "Thanks for Signing up" in response.json()["message"]
    # Clean up: remove the test user
    usersList[:] = [u for u in usersList if u["email"] != "testuser@example.com"]

def test_post_signup_validation():
    data = {"name": "", "email": "bad", "password": ""}
    response = client.post("/signup", data=data)
    assert response.status_code == 422

def test_post_signup_email_alrady_exist():
    data = {"name": "Yusuf", "email": "example@hotmail.com", "password": "password123"}
    response = client.post("/signup", data=data)
    assert response.status_code == 409
    assert "User with this email already exists" in response.json()["message"]

def test_post_login_success():
    # Use an existing user
    data = {"email": "example@hotmail.com", "password": "password123"}
    response = client.post("/login", data=data)
    assert response.status_code == 200
    assert "Log in successful" in response.json()["message"]

def test_post_login_user_not_found():
    data = {"email": "notfound@example.com", "password": "pass"}
    response = client.post("/login", data=data)
    assert response.status_code == 404
    assert "User not found" in response.json()["detail"]

def test_post_login_wrong_password():
    data = {"email": "example@hotmail.com", "password": "wrong"}
    response = client.post("/login", data=data)
    assert response.status_code == 401
    assert "Incorrect password" in response.json()["detail"]

def test_get_balance():
    # Log in first to set global state
    client.post("/login", data={"email": "example@hotmail.com", "password": "password123"})
    response = client.get("/balance")
    assert response.status_code == 200
    assert "balance" in response.json()

def test_post_send_transaction_insufficient():
    # Log in as user with low balance
    client.post("/login", data={"email": "example@outlook.com", "password": "password345"})
    response = client.post("/send_transaction", data={"to_account_id": 3, "amount": 9999})
    assert response.status_code == 400
    assert "Insufficient balance" in response.json()["detail"]

def test_post_send_transaction_success():
    # Log in as user with enough balance
    client.post("/login", data={"email": "example@hotmail.com", "password": "password123"})
    response = client.post("/send_transaction", data={"to_account_id": 3, "amount": 10})
    assert response.status_code == 200
    assert "Transaction of 10.0 to account 3 successful" in response.json()["message"]
    # Clean up: remove the test transaction
    all_transactions.pop()

def test_get_view_transactions():
    # Log in as user with transactions
    client.post("/login", data={"email": "example@hotmail.com", "password": "password123"})
    response = client.get("/view_transcaitons")
    assert response.status_code == 200
    assert isinstance(response.json(), list)