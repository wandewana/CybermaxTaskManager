# Cybermax Task Manager API

This is the backend service for the Cybermax Task Manager, a powerful and scalable task management application built with FastAPI. It features a modern, asynchronous architecture, secure user authentication, and a robust database setup.

## Table of Contents

- [Software Architecture](#software-architecture)
- [Project Structure](#project-structure)
- [Tools and Technologies](#tools-and-technologies)
- [Setup and Installation](#setup-and-installation)
- [Running the Application](#running-the-application)
- [Running Tests](#running-tests)
- [API Endpoints](#api-endpoints)

## Software Architecture

The application follows a containerized, service-oriented architecture:

- **Application Server**: A FastAPI application serves the main API. It's built to be fully asynchronous, from the web server down to the database, ensuring high performance.
- **Database**: A PostgreSQL 15 instance is used as the primary relational database, managed via SQLAlchemy and Alembic for migrations.
- **Cache/Broker**: Redis 7 is included for future use as a cache or a message broker for background tasks.
- **Containerization**: All services (PostgreSQL, Redis) are managed and run using Docker and Docker Compose, ensuring a consistent and reproducible development environment.

## Project Structure

The project is organized into logical modules to promote separation of concerns:

```
CybermaxTaskManager/
├── alembic/              # Alembic migration scripts
├── app/
│   ├── api/              # API endpoints and routing
│   │   ├── endpoints/
│   │   └── deps.py       # FastAPI dependencies (e.g., get_db)
│   ├── core/             # Core logic (security, JWT)
│   ├── db/               # Database session, models, and CRUD operations
│   ├── models/           # SQLAlchemy ORM models
│   ├── schemas/          # Pydantic schemas for data validation
│   └── main.py           # Main FastAPI application entrypoint
├── tests/                # Pytest tests
├── .gitignore
├── docker-compose.yml    # Docker service definitions
├── Dockerfile            # Dockerfile for the FastAPI app (if needed)
├── pytest.ini            # Pytest configuration
├── README.md
└── requirements.txt      # Python dependencies
```

## Tools and Technologies

- **Backend Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Database ORM**: [SQLAlchemy](https://www.sqlalchemy.org/) (with `asyncio` support)
- **Database Driver**: [asyncpg](https://github.com/MagicStack/asyncpg)
- **Database Migrations**: [Alembic](https://alembic.sqlalchemy.org/)
- **Data Validation**: [Pydantic](https://pydantic-docs.helpmanual.io/)
- **Authentication**: [python-jose](https://github.com/mpdavis/python-jose) for JWT, [passlib](https://passlib.readthedocs.io/en/stable/) for password hashing
- **Containerization**: [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/)
- **Testing**: [Pytest](https://docs.pytest.org/en/7.1.x/) with `pytest-asyncio` and `httpx`

## Setup and Installation

### Prerequisites

- [Python 3.10+](https://www.python.org/)
- [Docker](https://www.docker.com/products/docker-desktop/)

### Steps

1.  **Clone the repository (if you haven't already):**
    ```sh
    git clone <repository-url>
    cd CybermaxTaskManager
    ```

2.  **Install Python dependencies:**
    ```sh
    python -m pip install -r requirements.txt
    ```

3.  **Start the background services (PostgreSQL and Redis):**
    ```sh
    docker-compose up -d
    ```

4.  **Run the database migrations:**
    This command will create the `users` table in the database.
    ```sh
    alembic upgrade head
    ```

## Running the Application

To start the FastAPI development server, run the following command:

```sh
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.

## Running Tests

To run the automated tests, use `pytest`:

```sh
pytest -v
```

## API Endpoints

### Authentication

- **Register a new user:**
  ```sh
  Invoke-WebRequest -Uri "http://localhost:8000/auth/register" -Method POST -ContentType "application/json" -Body '{"email": "user@example.com", "password": "a-strong-password"}'
  ```

- **Log in to get access tokens:**
  ```sh
  Invoke-WebRequest -Uri "http://localhost:8000/auth/login" -Method POST -ContentType "application/json" -Body '{"email": "user@example.com", "password": "a-strong-password"}'
  ```

### Users

- **Get current user details (requires authentication):**
  ```powershell
  # First, log in to get a token
  $loginResponse = Invoke-WebRequest -Uri "http://localhost:8000/auth/login" -Method POST -ContentType "application/json" -Body '{"email": "user@example.com", "password": "a-strong-password"}'
  $token = ($loginResponse.Content | ConvertFrom-Json).access_token
  
  # Then, use the token to access the protected endpoint
  $headers = @{ "Authorization" = "Bearer $token" }
  Invoke-WebRequest -Uri "http://localhost:8000/users/me" -Method GET -Headers $headers
  ```
