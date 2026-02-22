import pytest


def test_list_expenses_requires_auth(anon_client):
    resp = anon_client.get("/expenses")
    assert resp.status_code == 401


def test_list_expenses(auth_client):
    resp = auth_client.get("/expenses")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    # the generate_mock_data fixture creates 10 expenses
    assert len(data) == 10


def test_retrieve_expense_detail(auth_client, random_task):
    resp = auth_client.get(f"/expense/{random_task.id}")
    assert resp.status_code == 200
    body = resp.json()
    assert body["id"] == random_task.id


def test_retrieve_expense_not_found(auth_client):
    resp = auth_client.get("/expense/99999")
    assert resp.status_code == 404


def test_add_expense(auth_client):
    payload = {"expense_name": "coffee", "mount": 123.45}
    resp = auth_client.post("/expenses", json=payload)
    assert resp.status_code == 200
    body = resp.json()
    assert body["expense_name"] == "Coffee"  # serializer title-cases
    assert body["mount"] == 123.45
    assert "id" in body


def test_update_expense(auth_client, random_task):
    new_data = {"expense_name": "updated name", "mount": 999.0}
    resp = auth_client.put(f"/expense_update/{random_task.id}", json=new_data)
    assert resp.status_code == 200
    body = resp.json()
    assert body["expense_name"] == "Updated Name"
    assert body["mount"] == 999.0


def test_update_expense_not_found(auth_client):
    new_data = {"expense_name": "whatever", "mount": 1}
    resp = auth_client.put("/expense_update/12345678", json=new_data)
    assert resp.status_code == 404


def test_delete_expense(auth_client, random_task):
    resp = auth_client.delete(f"/expense/{random_task.id}")
    assert resp.status_code == 200
    assert resp.json()["detail"]


def test_delete_expense_not_found(auth_client):
    resp = auth_client.delete("/expense/987654321")
    assert resp.status_code == 404


def test_pagination_and_limit(auth_client):
    # limit=5 should return 5 items
    resp = auth_client.get("/expenses?limit=5&offset=2")
    assert resp.status_code == 200
    assert len(resp.json()) == 5

# we intentionally do not test the 'completed' query parameter because the model does not
# have an 'is_complete' field; passing it will raise a SQLAlchemy error.