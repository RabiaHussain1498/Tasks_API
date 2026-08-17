# Full-Stack Notes Application

## Run locally

### 1) Start the backend

From the project root:

```bash
docker-compose down -v
docker-compose up -d
docker-compose exec api alembic upgrade head
```

Backend URL:

```text
http://localhost:8000
```

Swagger UI:

```text
http://localhost:8000/docs
```

### 2) Start the frontend

In a second terminal:

```bash
cd frontend
npm install
npm run dev -- --host 0.0.0.0
```

Frontend URL:

```text
http://localhost:5173
```

If port 5173 is already in use, Vite will automatically choose the next available port, for example:

```text
http://localhost:5174
```

Make sure the frontend env file contains:

```env
VITE_API_URL=http://localhost:8000
```

## Test flow

1. Register a user.
2. Log in.
3. Create a note.
4. Edit the note.
5. Delete the note.
6. Delete the same note again.
7. Try updating the same deleted note again.

Expected:
- valid create/update/delete should work
- second delete should return `404 Not Found`
- update on a deleted note should also return `404 Not Found`
- the app should show a real error message instead of failing silently

## Notes

This project uses FastAPI + PostgreSQL + React + Vite, with JWT auth and note CRUD operations.
