# FastAPI File Storage Service with MinIO and Celery

## Overview
This is a FastAPI-based file storage with MinIO for object storage and Celery for background task processing. It allows users to upload, process, and manage files via REST API.

## Features
- File upload (to MinIO, metadata saved in PostgreSQL)
- Background processing (Celery with Redis)
- JWT authentication (secure endpoints)
- File management (list, delete, presigned download URLs)


## Installation & Setup
1. Clone the repository
```bash
git clone https://github.com/yourusername/fastapi-file-storage.git
cd fastapi-file-storage
```

2. Create & activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Configure environment variables.
Copy the provided `.env.example` and rename it to `.env`.

Then edit `.env` and replace placeholder values:
```
# SECURITY WARNING!
# 1. Rename this to .env
# 2. Never commit real keys

# Django / FastAPI settings
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# MinIO settings (object storage)
MINIO_ENDPOINT=127.0.0.1:9000             # MinIO host and port
MINIO_ACCESS_KEY=admin                    # MinIO username
MINIO_SECRET_KEY=admin123                 # MinIO password
MINIO_BUCKET=file-storage                 # Bucket name for file uploads

# PostgreSQL database (via asyncpg driver for SQLAlchemy)
DATABASE_URL=postgresql+asyncpg://fastapi:fastapi@localhost/files_db
# Format: postgresql+asyncpg://<user>:<password>@<host>/<database>

# Redis (for background tasks with Celery)
REDIS_URL=redis://localhost:6379/0
```

5. Start PostgreSQL, Redis, Celery, and MinIO using Docker Compose
```bash
docker-compose up -d --build
```


6. Run database migrations
Before starting FastAPI, run database migrations:
```bash
alembic upgrade head
```

7. Start FastAPI server
```bash
uvicorn main:app --reload
```
API documentation available at: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)


## Tech stack
- **FastAPI**
- **PostgreSQL**
- **MinIO**
- **Celery + Redis**
- **Docker & Docker Compose**
- **Alembic** (migrations)
- **JWT Auth (via PyJWT or similar)**


## API Endpoints
### Authentication
| Method | Endpoint | Description |
|--------|---------|-------------|
| POST | `/auth/register/` | Register a new user |
| POST | `/auth/login/` | Login and receive JWT token |

### File Management
| Method | Endpoint | Description |
|--------|---------|-------------|
| POST | `/files/upload/` | Upload a file |
| GET  | `/files/` | List all files |
| GET  | `/files/download/{file_key}` | Get presigned URL for file download |
| DELETE | `/files/{file_key}` | Delete a file |

### Background Processing
| Method | Endpoint | Description |
|--------|---------|-------------|
| POST  | `/files/process/{file_name}` | Send file for processing |

## Author
**Valeriy Abramov**
- GitHub: [@abramov-v](https://github.com/abramov-v) 
- email: abramov.valeriy@hotmail.com
