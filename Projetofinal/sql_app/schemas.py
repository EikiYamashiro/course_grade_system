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


# class NotaBase(BaseModel):


# class NotaCreate(NotaBase):
#     pass


class Nota(BaseModel):
    id: int
    nome_disicplina: str
    descricao: str

    class Config:
        orm_mode = True
