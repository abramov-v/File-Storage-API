# File Storage API

## Overview
This is a FastAPI-based file storage with MinIO for object storage and Celery for background task processing. It allows users to upload, process, and manage files via REST API.

## Features
- File Upload: Store files in MinIO and record metadata in PostgreSQL.
- Background Processing: Uses Celery to process uploaded files asynchronously.
- User Authentication: Secure API with JWT-based authentication.
- File Management: List, delete, and download files.


## Installation & Setup
### Clone the repository
```bash
git clone https://github.com/yourusername/fastapi-file-storage.git
cd fastapi-file-storage
```

### Create & activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### Install dependencies
```bash
pip install -r requirements.txt
```

### Configure environment variables
Create `.env` file in the root directory and set the following variables:
```
SECRET_KEY=secretkey
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
MINIO_ENDPOINT=http://127.0.0.1:9000
MINIO_ACCESS_KEY=admin
MINIO_SECRET_KEY=admin123
MINIO_BUCKET=file-storage
DATABASE_URL=postgresql+asyncpg://fastapi:fastapi@localhost/files_db
REDIS_URL=redis://localhost:6379/0
```

### Start PostgreSQL, Redis, Celery, and MinIO using Docker Compose
```bash
docker-compose up -d --build
```


### Run database migrations
Before starting FastAPI, run database migrations:
```bash
alembic upgrade head
```

### Start FastAPI server
```bash
uvicorn main:app --reload
```
API documentation available at: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)


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

## Running with Docker Compose (for databases and Celery)

To run PostgreSQL, Redis, MinIO, and Celery Worker:
```bash
docker-compose up -d --build
```

To stop all containers:
```bash
docker-compose down
```

## Author
**Valeriy Abramov**
- GitHub: [@abramov-dev](https://github.com/abramov-dev) 
- email: abramov.valeriy@hotmail.com