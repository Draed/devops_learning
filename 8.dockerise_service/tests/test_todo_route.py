import pytest
from app.main import app

def test_create_todo(test_client):
    response = test_client.post("/todos/", json={"id": 1, "title": "Learn FastAPI"})
    assert response.status_code == 200
    assert response.json() == {"id": 1, "title": "Learn FastAPI", "completed": False}

def test_get_todos(test_client):
    # Create a todo first
    test_client.post("/todos/", json={"id": 2, "title": "Write tests"})
    response = test_client.get("/todos/")
    assert response.status_code == 200
    # assert len(response.json()) == 2

def test_get_todo(test_client):
    test_client.post("/todos/", json={"id": 1, "title": "Learn FastAPI", "completed": False})
    response = test_client.get("/todos/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "title": "Learn FastAPI", "completed": False}
    
    # Test getting a non-existent todo
    response = test_client.get("/todos/99")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Todo not found'}

# def test_update_todo(test_client):
#     response = test_client.put("/todos/1", json={"id": 1, "title": "Learn FastAPI and Pydantic", "completed": True})
#     assert response.status_code == 200
#     assert response.json() == {"id": 1, "title": "Learn FastAPI and Pydantic", "completed": True}

def test_delete_todo(test_client):
    test_client.post("/todos/", json={"id": 1, "title": "Learn FastAPI", "completed": False})
    response = test_client.delete("/todos/1")
    assert response.status_code == 200
    response = test_client.get("/todos/1")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Todo not found'}
