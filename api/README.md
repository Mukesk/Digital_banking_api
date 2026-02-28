# Digital Banking API

A digital banking backend application built using modern Python technologies.

## Features

- **User Accounts & Authentication:** Registration and JWT-based secure login.
- **Account Management:** Role-Based Access Control (RBAC) allowing creation of accounts and administrative freezing/deletions.
- **Fund Transfers:** Concurrent transfer execution using Redis-based distributed locking to guarantee ACID properties under load.
- **Loan Applications:** Customers can apply for loans, and officers can review and approve them. If approved, loan amounts are automatically disbursed to the user's active account.
- **Admin Reporting:** Aggregated administrative summaries of banking data.
- **Security & Reliability:** IP-based rate limiting, custom exception handling, request logging, and CORS middleware setup.

## Tech Stack
- **Framework:** FastAPI
- **Database:** PostgreSQL (with SQLAlchemy and Alembic for migrations)
- **Caching & Locks:** Redis
- **Authentication:** `python-jose` (JWT) and `passlib` (Bcrypt)
- **Testing:** `pytest` (with a fast in-memory SQLite configuration)
- **Deployment:** Docker & Docker Compose

## Quick Start (Local Setup)

### 1. Requirements
Ensure you have Python 3.11+, `pip`, and `docker` installed on your machine.

### 2. Environment Variables
Copy `.env.example` to `.env` (or create a `.env` file) and provide the following configuration:
```env
DATABASE_URL=postgresql://banking_user:banking_pass@localhost:5432/banking_db
SECRET_KEY=your-super-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30
REDIS_URL=redis://localhost:6379
POSTGRES_USER=banking_user
POSTGRES_PASSWORD=banking_pass
POSTGRES_DB=banking_db
```

### 3. Start Database Infrastructure (Postgres & Redis)
```bash
docker-compose up -d
```

### 4. Create Virtual Environment & Install Dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 5. Run Database Migrations
Create the required tables via Alembic:
```bash
alembic upgrade head
```

### 6. Start the API Server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 7. Interactive Documentation
After starting the server, you can interface directly with the API endpoints using the auto-generated Swagger documentation at:
- [http://localhost:8000/docs](http://localhost:8000/docs)

## Running Tests
To run the automated tests using an isolated, in-memory SQLite database:
```bash
PYTHONPATH=. pytest
```
