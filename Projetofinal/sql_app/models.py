from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from uuid import UUID

from database import Base


class Disciplina(Base):
    __tablename__ = "disciplina"

    nome = Column(String, primary_key=True, index=True)
    nome_professor = Column(String, index=True)
    sobrenome_professor = Column(String, index=True)
    anotacao = Column(String, index=True)

    nota = relationship("Nota", back_populates="disciplina")


class Nota(Base):
    __tablename__ = "nota"
    # Acho que a gente vai mexer aqui

    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String, index=True)
    nome_disciplina = Column(String, ForeignKey("disciplina.nome"))

    disciplina = relationship("Disciplina", back_populates="nota")
