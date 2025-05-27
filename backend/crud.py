from sqlalchemy.orm import Session # representa uma sessão ativa no banco
from database import Note # representa a tabela notes
from models import NoteCreate, NoteUpdate # modelos pydantic que validam os dados de entrada na criação e validação

# realiza uma consulta na tabela notes e retorna todas as notas
def get_notes(db: Session):
    return db.query(Note).all()

# criar nota
def create_note(db: Session, note: NoteCreate, image_path: str = None):
    # instância do modelo ORM:
    db_note = Note(
        title=note.title,
        description=note.description,
        image=image_path,
        completed=False
    )
    db.add(db_note) # adiciona o objeto à sessão
    db.commit() # salva no banco de dados
    db.refresh(db_note) # atualiza do db_note com os dados gerados
    return db_note # retorna o objeto criado

# atualizar nota
def update_note(db: Session, note_id, note: NoteUpdate):
    db_note = db.query(Note).filter(Note.id == note_id).first() # busca nota pelo referido id
    # atualiza os dados da nota:
    if db_note:
        db_note.title = note.title
        db_note.description = note.description
        db_note.completed = note.completed
        # salva os novos dados da nota no banco
        db.commit()
        db.refresh(db_note)
    return db_note # retorna a nota atualizada

def delete_note(db: Session, note_id: int):
    db_note = db.query(Note).filter(Note.id == note_id).first() # busca nota pelo referido id
    # remove a nota (se achar):
    if db_note:
        db.delete(db_note)
        db.commit()
    return db_note # retorna o objeto deletado (útil para a api informar que foi removido)