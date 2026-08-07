from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from database import Base, engine
from dependencies import get_db, get_current_user
from models import Note, User
from schemas import NoteCreate, UserCreate
from auth import create_access_token


Base.metadata.create_all(bind=engine)

app = FastAPI()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@app.get("/")
def home():
    return {"message": "Notes API is running"}


# REGISTER user
@app.post("/api/v1/register", status_code=201)
def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    hashed_password = pwd_context.hash(user_data.password)
    user = User(
        username=user_data.username,
        hashed_password=hashed_password
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return {"id": user.id, "username": user.username}


# LOGIN
@app.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == form_data.username).first()

    if user is None or not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_access_token(data={"sub": user.username})

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@app.post("/api/v1/notes", status_code=201)
def create_note(
    note: NoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_note = Note(
        title=note.title,
        body=note.body,
        owner_id=current_user.id,
        category_id=note.category_id
    )

    db.add(new_note)
    db.commit()
    db.refresh(new_note)

    return new_note


@app.get("/api/v1/notes")
def get_notes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    notes = db.query(Note).filter(
        Note.owner_id == current_user.id
    ).all()

    return notes


@app.get("/api/v1/notes/{note_id}")
def get_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    note = db.query(Note).filter(
        Note.id == note_id,
        Note.owner_id == current_user.id
    ).first()

    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    return note


@app.put("/api/v1/notes/{note_id}")
def update_note(
    note_id: int,
    note: NoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    existing_note = db.query(Note).filter(
        Note.id == note_id,
        Note.owner_id == current_user.id
    ).first()

    if existing_note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    existing_note.title = note.title
    existing_note.body = note.body
    existing_note.category_id = note.category_id

    db.commit()
    db.refresh(existing_note)

    return existing_note


@app.delete("/api/v1/notes/{note_id}", status_code=204)
def delete_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    note = db.query(Note).filter(
        Note.id == note_id,
        Note.owner_id == current_user.id
    ).first()

    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    db.delete(note)
    db.commit()

    return None