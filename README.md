# Python Task Management API

## Project Overview

A beginner-friendly REST API developed with Python and FastAPI. The application allows users to create, retrieve, update, and delete tasks through HTTP requests.

It uses SQLite for persistent data storage and SQLAlchemy for database operations.

This project demonstrates foundational software engineering skills, including REST API development, database integration, input validation, error handling, and automated testing.

## Features

- Create new tasks
- Retrieve all tasks
- Retrieve a task by ID
- Update existing tasks using PATCH
- Delete tasks
- Health-check endpoint
- SQLite database integration
- SQLAlchemy ORM for database operations
- Input validation using Pydantic
- HTTP error handling (400, 404, and 422)
- Automated testing with Pytest
- Isolated test database for reliable testing

## Technologies

- Python 3.12
- FastAPI
- SQLAlchemy
- SQLite
- Uvicorn
- Pydantic
- Pytest
- HTTPX
- Git and GitHub

## Project Structure

```text
Python-Task-Management-API/
├── main.py
├── database.py
├── models.py
├── requirements.txt
├── pytest.ini
├── .gitignore
├── README.md
└── tests/
    ├── conftest.py
    └── test_tasks.py
```

The SQLite database file is created locally when the application runs and is excluded from GitHub using `.gitignore`.

## Installation

Clone the repository:

```bash
git clone https://github.com/cybertraining07/Python-Task-Management-API.git
cd Python-Task-Management-API
```

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the Application

Start the development server:

```bash
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8001
```

Open the interactive API documentation:

http://127.0.0.1:8001/docs

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Welcome message |
| GET | `/health` | Health check |
| POST | `/tasks` | Create a task |
| GET | `/tasks` | Retrieve all tasks |
| GET | `/tasks/{task_id}` | Retrieve a task by ID |
| PATCH | `/tasks/{task_id}` | Update a task |
| DELETE | `/tasks/{task_id}` | Delete a task |

## Example Task

Create a task using the POST `/tasks` endpoint:

```json
{
  "title": "Learn FastAPI",
  "description": "Build my first REST API",
  "completed": false
}
```

## Automated Testing

Run the test suite:

```bash
pytest -v
```

**Latest test result: 19 tests passed.**

The test suite covers:

- API health checks
- Task creation and retrieval
- Task updates and deletion
- Missing task handling
- Empty and invalid task titles
- Description length validation
- Empty update requests
- Null title validation

Tests use a separate temporary SQLite database to avoid modifying the application's local database.

## Learning Outcomes

Through this project, I practiced:

- Building REST APIs with Python and FastAPI
- Implementing CRUD operations
- Working with relational databases using SQLAlchemy
- Validating API input with Pydantic
- Handling HTTP errors
- Writing automated tests with Pytest
- Using Git and GitHub for version control

## Project Repository

GitHub: https://github.com/cybertraining07/Python-Task-Management-API

## Project Scope

This is an educational portfolio project developed to demonstrate foundational Python backend development skills. It is not intended to be a production-ready application.
