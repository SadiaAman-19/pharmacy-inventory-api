# Pharmacy Inventory REST API

A CRUD REST API built with Python, FastAPI and SQLite, tested with Postman.

## Run
1. pip install -r requirements.txt
2. python -m uvicorn main:app --reload --port 3000
3. python seed.py   (loads 12 sample medicines)

API: http://localhost:3000/api/medicines
Docs: http://localhost:3000/docs

## Endpoints
POST /api/medicines, GET /api/medicines, GET /api/medicines/{id}, PUT /api/medicines/{id}, DELETE /api/medicines/{id}