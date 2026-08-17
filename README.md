# Full-Stack Notes Application

This project is a complete full-stack CRUD application featuring a Python FastAPI backend and a React (Vite) frontend. It allows users to securely register, log in using JWT authentication, and manage their personal notes.

## Project Structure

- **Backend (`/`)**: A FastAPI application using SQLAlchemy and PostgreSQL for database management. Includes JWT authentication, password hashing (bcrypt), and full RESTful endpoints for Users, Notes, and Categories.
- **Frontend (`/frontend`)**: A React application built with Vite. It features a modern, flat-design dark mode UI with glassmorphism-inspired solid panels. Handles authentication state, API communication, and dynamic UI updates without page reloads.

## Prerequisites

- Python 3.10+
- Node.js & npm
- PostgreSQL (or SQLite for local development)

## Setup Instructions

### 1. Run the backend with Docker

From the project root:

```bash
docker-compose down -v
docker-compose up -d
docker-compose exec api alembic upgrade head
```

This resets the PostgreSQL volume, starts the API and database containers, and applies the latest Alembic migration.

The backend runs on:

```text
http://localhost:8000
```

Swagger docs are available at:

```text
http://localhost:8000/docs
```

### 2. Run the frontend

Open a second terminal and run:

```bash
cd frontend
npm install
npm run dev -- --host 0.0.0.0
```

The frontend will run on the Vite URL printed in the terminal, typically:

```text
http://localhost:5173
```

Make sure the frontend env file exists and contains:

```env
VITE_API_URL=http://localhost:8000
```

### 3. Test the app manually

1. Open the frontend in the browser.
2. Register a new user.
3. Log in.
4. Create a note.
5. Update the note.
6. Delete the note.
7. Delete the same note again.
8. Try updating the same deleted note again.

Expected result:
- create, update, and delete should succeed for valid notes
- second delete should return `404 Not Found`
- update on a deleted note should also return `404 Not Found`
- the app should show a real error message instead of crashing silently

### 4. Optional local Python-only setup

If you want to run the backend without Docker for local development:

```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
pip install -r requirements.txt
uvicorn main:app --reload
```

Then create a `.env` file from `.env.example` and set the database URL and secret key.

## Features

- **JWT Authentication**: Secure login flow protecting all note routes.
- **Full CRUD**: Create, Read, Update, and Delete notes.
- **Optimistic UI**: The React state updates instantly without needing to refetch the entire list from the server after every change.
- **Error Handling**: Graceful error handling for `404 Not Found` (e.g., if a note was deleted in another tab) and `401 Unauthorized` (expired tokens).
- **Modern Design**: Completely custom CSS featuring a cohesive dark mode color palette.
