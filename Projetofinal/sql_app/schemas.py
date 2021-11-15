from typing import List, Optional

from pydantic import BaseModel
from uuid import UUID


# class DisciplinaBase(BaseModel):
#     nome_professor: Optional[str] = None
#     sobrenome_professor: Optional[str] = None


# class DisciplinaCreate(DisciplinaBase):
#     pass


class Disciplina(BaseModel):
    nome: str
    nome_professor: Optional[str] = None
    sobrenome_professor: Optional[str] = None

    class Config:
        orm_mode = True


class NotaCreate(BaseModel):
    id: int
    descricao: str


class Nota(NotaCreate):
    nome_disicplina: str

    class Config:
        orm_mode = True
