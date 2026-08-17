# Database Schema Design

## Overview
The Notes API uses PostgreSQL with SQLAlchemy ORM. The database consists of three main entities: Users, Notes, and Categories.

---

## Database Tables

### 1. users Table
Stores user account information for authentication.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | Integer | Primary Key, Auto-increment | Unique user identifier |
| username | String | Unique, Not Null, Indexed | User login username |
| hashed_password | String | Not Null | Bcrypt hashed password |

```python
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
```

---

### 2. categories Table
Stores note categories for organizing notes.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | Integer | Primary Key, Auto-increment | Unique category identifier |
| name | String | Not Null | Category name |

Relationships:
- One-to-Many with Note table

```python
class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    notes = relationship("Note", back_populates="category")
```

---

### 3. notes Table
Stores user notes with metadata.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | Integer | Primary Key, Auto-increment | Unique note identifier |
| title | String | Not Null | Note title |
| body | String | Not Null | Note content |
| owner_id | Integer | Not Null, Foreign Key | User who owns the note |
| category_id | Integer | Foreign Key, Nullable | Associated category |
| created_at | DateTime | Default: UTC now | Creation timestamp |

Relationships:
- Many-to-One with Category table
- Many-to-One with User table (owner)

```python
class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    body = Column(String, nullable=False)
    owner_id = Column(Integer, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    category = relationship("Category", back_populates="notes")
```

---

## Pydantic Schemas

Used for request/response validation and documentation.

### UserCreate
For user registration

```python
class UserCreate(BaseModel):
    username: str
    password: str
```

### NoteCreate
For creating and updating notes

```python
class NoteCreate(BaseModel):
    title: str
    body: str
    category_id: Optional[int] = None
```

### CategoryCreate
For creating categories

```python
class CategoryCreate(BaseModel):
    name: str
```

---

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and get JWT token

### Notes
- `GET /api/v1/notes` - List all user notes (requires auth)
- `POST /api/v1/notes` - Create new note (requires auth)
- `GET /api/v1/notes/{id}` - Get specific note (requires auth)
- `PUT /api/v1/notes/{id}` - Update note (requires auth)
- `DELETE /api/v1/notes/{id}` - Delete note (requires auth)

### Categories
- `GET /api/v1/categories` - List all categories (requires auth)
- `POST /api/v1/categories` - Create new category (requires auth)

---

## Authentication Flow

1. User registers with username and password
2. Password is hashed with bcrypt before storing
3. User logs in and receives JWT token
4. Token is included in Authorization header for authenticated endpoints
5. JWT contains username claim ("sub") and expiration (30 minutes)

### Request Headers
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json
```

---

## Data Relationships

```
User (1) ----< (Many) Note
           |
           +-- owner_id (Foreign Key)

Category (1) ----< (Many) Note
                  |
                  +-- category_id (Foreign Key)
```

- Each Note belongs to exactly one User (owner)
- Each Note can belong to zero or one Category
- Each Category can have multiple Notes
- Each User can have multiple Notes

---

## Database Migrations

Managed by Alembic. Current migration:
- `alembic/versions/774472689fb2_create_task_and_category_tables.py`

To create new migrations:
```bash
alembic revision --autogenerate -m "description of changes"
alembic upgrade head
```
