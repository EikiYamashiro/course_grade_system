from sqlalchemy.orm import Session
from uuid import UUID

import models
import schemas


def get_notas(db: Session, nome: str):
    return db.query(models.Nota).filter(models.Nota.nome_disciplina == nome).all()


def get_disciplina(db: Session, nome: str):
    return db.query(models.Disciplina).filter(models.Disciplina.nome == nome).first()


def get_name_disciplinas(db: Session):
    return db.query(models.Disciplina).all()


def get_index_nota(db: Session, nome: str):
    return db.query(models.Nota).filter(models.Nota.nome_disciplina == nome).all()


def create_nota(db: Session, nota: schemas.NotaCreate, disciplina: str):
    db_nota = models.Nota(
        id=nota.id, descricao=nota.descricao, nome_disciplina=disciplina)
    db.add(db_nota)
    db.commit()
    db.refresh(db_nota)
    return db_nota


def delete_nota(db: Session, nome: str, id: int):
    # id = str(id)
    db_nota = db.query(models.Nota).filter(
        models.Nota.nome_disciplina == nome, models.Nota.id == id).one_or_none()
    if db_nota is None:
        return False
    db.query(models.Nota).filter(models.Nota.nome_disciplina ==
                                 nome, models.Nota.id == id).delete()
    db.commit()
    return True

# def get_items(db: Session, skip: int = 0, limit: int = 100):
    # return db.query(models.Item).offset(skip).limit(limit).all()


def create_discipline(db: Session, disciplina: schemas.Disciplina):
    db_discipline = models.Disciplina(**disciplina.dict())
    db.add(db_discipline)
    db.commit()
    db.refresh(db_discipline)
    return db_discipline


def delete_discipline(db: Session, nome: str):
    db.query(models.Disciplina).filter(models.Disciplina.nome == nome).delete()
    db.commit()
    return {"Detail": "Disciplina deletada com sucesso"}


def update_discipline(db: Session, disciplina: schemas.Disciplina, nome: str):
    db_discipline = db.query(models.Disciplina).filter(
        models.Disciplina.nome == nome).one_or_none()

    if db_discipline is None:
        return None

    for var, value in vars(disciplina).items():
        setattr(db_discipline, var, value) if value else None
        print(var, value)

    db.add(db_discipline)
    db.commit()
    db.refresh(db_discipline)
    return db_discipline


def update_nota(db: Session, nota: schemas.Nota, nome: str):
    db_nota = db.query(models.Nota).filter(
        models.Nota.nome_disciplina == nome).one_or_none()

    if db_nota is None:
        return None

    for var, value in vars(nota).items():
        setattr(db_nota, var, value) if value else None
        print(var, value)

    db.add(db_nota)
    db.commit()
    db.refresh(db_nota)
    return db_nota
