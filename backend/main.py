from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends # gerenciam dados de forms e arquivos enviados, e httpexception gera respostas de erro HTTP
from fastapi.middleware.cors import CORSMiddleware # permite o front acessar a api
from fastapi.staticfiles import StaticFiles # para arquivos estáticos (img)
from sqlalchemy.orm import Session 

# manipulação de arquivos e sistema operacional
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import shutil

from database import create_db, SessionLocal
import crud
import models


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

create_db()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# pasta de uploads
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=UPLOAD_FOLDER), name="uploads")

@app.get("/notes/")
def read_note(
    title: str = Form(...),
    description: str = Form(...),
    file: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    image_path = None
    if file:
        file_location = f"{UPLOAD_FOLDER}/{file.filename}"
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(file.file, file_object)
        image_path = file_location

    note = models.NoteCreate(title=title, description=description)
    return crud.create_note(db, note, image_path)

@app.put("/notes/{notes_id}")
def update_note(note_id: int, note: models.NoteUpdate, db: Session = Depends(get_db)):
    updated = crud.update_note(db, note_id, note)
    if not updated:
        raise HTTPException(status_code=404, detail="Nota não encontrada")
    return updated

@app.delete("/notes/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_note(db, note_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Nota não encontrada")
    return deleted

