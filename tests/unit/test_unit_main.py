import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
import pytest
from fastapi.testclient import TestClient
from app.main import app, usersList, all_transactions

client = TestClient(app)


from app.main import process_transaction

def test_process_transaction_success():
    users = [{"id": 1, "email": "a@b.com", "balance": 100}, {"id": 2, "email": "b@c.com", "balance": 100}]
    all_tx = []
    user_tx = []
    result = process_transaction(
        logged_in_user="a@b.com",
        user_balance=100,
        usersList=users,
        all_transactions=all_tx,
        user_transactions=user_tx,
        to_account_id=2,
        amount=50
    )
    assert "message" in result
    assert users[0]["balance"] == 50
    assert all_tx[0]["To Account"] == 2
    assert user_tx[0]["Amount"] == 50

def test_process_transaction_insufficient_balance():
    users = [{"id": 1, "email": "a@b.com", "balance": 30}, {"id": 2, "email": "b@c.com", "balance": 100}]
    all_tx = []
    user_tx = []
    result = process_transaction(
        logged_in_user="a@b.com",
        user_balance=30,
        usersList=users,
        all_transactions=all_tx,
        user_transactions=user_tx,
        to_account_id=2,
        amount=50
    )
    assert "error" in result
    assert result["error"] == "Insufficient balance"
    assert users[0]["balance"] == 30
    assert all_tx == []
    assert user_tx == []