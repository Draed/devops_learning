#!/usr/bin/env bash

## Description : A simple test shell script that test TODO app

echo "== Adding a first todo"
curl -s -w "\n HTTP CODE : %{http_code}\n" -X POST "http://127.0.0.1:8000/todos/" -H "Content-Type: application/json" -d '{ "id": 1, "title": "Discover FastAPI" }'
echo ""
echo "== Adding a second todo"
curl -s -w "\n HTTP CODE : %{http_code}\n" -X POST "http://127.0.0.1:8000/todos/" -H "Content-Type: application/json" -d '{ "id": 2, "title": "Learn more about FastAPI" }'
echo ""
echo "== Reading all todo "
curl -s -w "\n HTTP CODE : %{http_code}\n" -X GET "http://127.0.0.1:8000/todos/"
echo ""
echo "== Reading only one todo "
curl -s -w "\n HTTP CODE : %{http_code}\n" -X GET "http://127.0.0.1:8000/todos/1"
echo ""
echo "== Deleting a todo "
curl -s -w "\n HTTP CODE : %{http_code}\n" -X DELETE "http://127.0.0.1:8000/todos/1"
echo ""
echo "More 'strange case' testing"
echo ""

echo "== Adding a todo with invalid field key"
curl -s -w "\n HTTP CODE : %{http_code}\n" -X POST "http://127.0.0.1:8000/todos/" -H "Content-Type: application/json" -d '{ "id": 1, "task": "Discover FastAPI" }'
echo ""
echo "== Adding a todo with invalid field value format"
curl -s -w "\n HTTP CODE : %{http_code}\n" -X POST "http://127.0.0.1:8000/todos/" -H "Content-Type: application/json" -d '{ "id": "test", "title": 1234 }'
echo ""
echo "== Try to read an not existing todo "
curl -s -w "\n HTTP CODE : %{http_code}\n" -X GET "http://127.0.0.1:8000/todos/10"
echo ""
echo "== Add a todo with an existing id "
curl -s -w "\n HTTP CODE : %{http_code}\n" -X POST "http://127.0.0.1:8000/todos/" -H "Content-Type: application/json" -d '{ "id": 2, "title": "Existing todo" }'
echo ""

echo "== Deleting all todos "
existing_todo_list=$(curl -s -X GET "http://127.0.0.1:8000/todos/")
mapfile -t values < <(echo "$existing_todo_list" | jq -r '.[].id')
for value in "${values[@]}"; do
    echo "Deleting todo with id : '${value}'"
    curl -s -w "\n HTTP CODE : %{http_code}\n" -X DELETE "http://127.0.0.1:8000/todos/${value}"
done
echo ""