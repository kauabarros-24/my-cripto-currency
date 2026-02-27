import pytest
from fastapi.testclient import TestClient
from src.main import app  # ajuste se seu arquivo tiver outro nome

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Blockchain node running"


def test_new_transaction():
    data = {
        "sender": "alice",
        "recipient": "bob",
        "amount": 10
    }

    response = client.post("/transactions/new", json=data)

    assert response.status_code == 200
    assert "Transaction will be added" in response.json()["message"]


def test_mine_block():
    response = client.get("/mine")

    assert response.status_code == 200
    body = response.json()

    assert body["message"] == "New Block Forged"
    assert "block" in body


def test_full_chain():
    response = client.get("/chain")

    assert response.status_code == 200
    body = response.json()

    assert "chain" in body
    assert "length" in body
    assert isinstance(body["chain"], list)


def test_register_nodes():
    data = {
        "nodes": [
            "http://localhost:5000",
            "http://localhost:5001"
        ]
    }

    response = client.post("/nodes/register", json=data)

    assert response.status_code == 200
    assert "total_nodes" in response.json()


def test_register_nodes_empty():
    response = client.post("/nodes/register", json={"nodes": []})

    assert response.status_code == 400


def test_consensus():
    response = client.get("/nodes/resolve")

    assert response.status_code == 200
    assert "message" in response.json()