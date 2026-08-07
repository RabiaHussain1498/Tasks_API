from dependencies import get_current_user
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal
from models import Note, User
from schemas import NoteCreate
from auth import create_access_token
import models
from passlib.context import CryptContext



Base.metadata.create_all(bind=engine)

app = FastAPI()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# REGISTER user
@app.post("/api/v1/register", status_code=201)
def register_user(
    user_data: dict,
    db: Session = Depends(get_db)
):
    if "username" not in user_data or "password" not in user_data:
        raise HTTPException(status_code=422, detail="Username and password required")
        
    existing_user = db.query(User).filter(User.username == user_data["username"]).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")


    print("PASSWORD RECEIVED:", user_data["password"])
    print("PASSWORD LENGTH:", len(user_data["password"]))

    hashed_password = pwd_context.hash(user_data["password"])    
   # hashed_password = pwd_context.hash(user_data["password"])
    user = User(
        username=user_data["username"],
        hashed_password=hashed_password
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return {"id": user.id, "username": user.username}


@app.get("/")
def home():
    return {
        "message": "Notes API is running"
    }


@app.post("/api/v1/notes", status_code=201)
def create_note(
    note: NoteCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    new_note = Note(
        title=note.title,
        body=note.body,
        owner_id=current_user["user_id"],
        category_id=note.category_id
    )

    db.add(new_note)
    db.commit()
    db.refresh(new_note)

    return new_note


@app.get("/api/v1/notes")
def get_notes(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    notes = db.query(Note).filter(
        Note.owner_id == current_user["user_id"]
    ).all()

    return notes


@app.get("/api/v1/notes/{note_id}")
def get_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    note = db.query(Note).filter(
        Note.id == note_id,
        Note.owner_id == current_user["user_id"]
    ).first()

    if note is None:
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )

    return note


@app.put("/api/v1/notes/{note_id}")
def update_note(
    note_id: int,
    note: NoteCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    existing_note = db.query(Note).filter(
        Note.id == note_id,
        Note.owner_id == current_user["user_id"]
    ).first()

    if existing_note is None:
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )

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
    current_user=Depends(get_current_user)
):

    note = db.query(Note).filter(
        Note.id == note_id,
        Note.owner_id == current_user["user_id"]
    ).first()

    if note is None:
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )

    db.delete(note)
    db.commit()

    return None


@app.post("/login")
def login(
    username: str,
    password: str,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.username == username
    ).first()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    if not pwd_context.verify(
        password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    token = create_access_token(
        {
            "user_id": user.id,
            "username": user.username
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }