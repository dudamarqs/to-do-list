from pydantic import BaseModel # validação de dados e serialização (requisições e respostas da api)
from typing import Optional # indica que um campo pode ser none (opcional)

# modelo base que define os campos comuns
class NoteBase(BaseModel):
    title: str
    description: str

# criação de nota
class NoteCreate(NoteBase):
    pass

# atualização de nota
class NoteUpdate(NoteBase):
    completed: bool
    
# representa como os dados serão retornados pela api ao usuário
class Note(NoteBase):
    id: int
    completed: bool
    image: Optional[str]

    # permite que o pydantic aceite os objetos do aqlalchemy diretamente, além de dicionários (dict)
    class Config:
        from_attributes = True