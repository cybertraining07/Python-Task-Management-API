
# Python Task Management API

## Project Overview

A beginner-friendly REST API built with Python and FastAPI. It allows users to create, retrieve, update, and delete tasks using HTTP requests.

The application uses SQLite for persistent data storage and SQLAlchemy for database operations.

## Features

- Create new tasks
- Retrieve all tasks
- Retrieve a task by ID
- Update existing tasks
- Delete tasks
- Health-check endpoint
- SQLite database integration
- Automated tests using Pytest
- Isolated test database

## Technologies

- Python 3.12
- FastAPI
- SQLAlchemy
- SQLite
- Uvicorn
- Pytest
- HTTPX
- Git

## Project Structure

```text
Python-Task-Management-API/
├── main.py
├── database.py
├── models.py
├── tasks.db
├── requirements.txt
├── pytest.ini
├── .gitignore
└── tests/
    ├── conftest.py
    └── test_tasks.py
```

## Installation

Clone the repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Python-Task-Management-API
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the Application

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8001
```

Open the interactive API documentation:

http://127.0.0.1:8001/docs

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | / | Welcome message |
| GET | /health | Health check |
| POST | /tasks | Create a task |
| GET | /tasks | Retrieve all tasks |
| GET | /tasks/{task_id} | Retrieve one task |
| PATCH | /tasks/{task_id} | Update a task |
| DELETE | /tasks/{task_id} | Delete a task |

## Run Automated Tests

```bash
pytest -v
```

The current test suite contains eight automated tests covering the main API functionality.

## Learning Outcomes

- Building REST APIs with FastAPI
- Working with HTTP methods and status codes
- Using SQLAlchemy ORM
- Integrating SQLite databases
- Implementing CRUD functionality
- Writing automated tests
- Managing Python dependencies
- Organizing a Python project

## Project Status

Core API functionality and eight automated tests have been implemented and verified.

## Disclaimer

This project is an educational portfolio project and is not intended as a production-ready service.
