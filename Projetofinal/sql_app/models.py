from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from uuid import UUID

from database import Base


class Disciplina(Base):
    __tablename__ = "disciplina"

    nome = Column(String(25), primary_key=True, index=True)
    nome_professor = Column(String(25), index=True)
    sobrenome_professor = Column(String(25), index=True)
    anotacao = Column(String(100), index=True)

    nota = relationship("Nota", back_populates="disciplina")


class Nota(Base):
    __tablename__ = "nota"

    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String(25), index=True)
    nome_disciplina = Column(String(25), ForeignKey("disciplina.nome"))

    disciplina = relationship("Disciplina", back_populates="nota")
