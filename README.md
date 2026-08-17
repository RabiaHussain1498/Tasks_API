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

### 1. Backend Setup (FastAPI)

1. Open a terminal in the root directory (`Tasks_API`).
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up your environment variables:
   Copy `.env.example` to a new file named `.env` and fill in your database credentials and secret key.
5. Start the server:
   ```bash
   uvicorn main:app --reload
   ```
   The backend will run on `http://localhost:8000`.

### 2. Frontend Setup (React)

1. Open a *second* terminal and navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Ensure your frontend `.env` file exists and points to the backend:
   ```env
   VITE_API_URL=http://localhost:8000
   ```
4. Start the development server:
   ```bash
   npm run dev
   ```
   The frontend will run on `http://localhost:5173`.

## Features

- **JWT Authentication**: Secure login flow protecting all note routes.
- **Full CRUD**: Create, Read, Update, and Delete notes.
- **Optimistic UI**: The React state updates instantly without needing to refetch the entire list from the server after every change.
- **Error Handling**: Graceful error handling for `404 Not Found` (e.g., if a note was deleted in another tab) and `401 Unauthorized` (expired tokens).
- **Modern Design**: Completely custom CSS featuring a cohesive dark mode color palette.
