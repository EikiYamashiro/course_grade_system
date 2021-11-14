from sqlalchemy.orm import Session
from uuid import UUID

from . import models, schemas


def get_nota(db: Session, nota_id: int):
    return db.query(models.Nota).filter(models.Nota.id == int).first()


def get_disciplina(db: Session, nome: str):
    return db.query(models.Disciplina).filter(models.Disciplina.nome == nome).first()


def get_name_disciplinas(db: Session):
    return db.query(models.Disciplina).all()


# def get_user_by_email(db: Session, email: str):
#     return db.query(models.User).filter(models.User.email == email).first()


# def get_users(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.User).offset(skip).limit(limit).all()


# def create_user(db: Session, user: schemas.UserCreate):
#     fake_hashed_password = user.password + "notreallyhashed"
#     db_discipline = models.User(
#         email=user.email, hashed_password=fake_hashed_password)
#     db.add(db_discipline)
#     db.commit()
#     db.refresh(db_discipline)
#     return db_discipline

def create_nota(db: Session, nota: schemas.Nota):
    db_nota = models.Nota(
        id=nota.id, descricao=nota.descricao)
    db.add(db_nota)
    db.commit()
    db.refresh(db_nota)
    return db_nota


# def delete_nota(db: Session, nota: schemas.NotaDelete):
#     db_nota = models.Nota(
#         id=nota.id, descricao=nota.descricao)
#     db.add(db_nota)
#     db.commit()
#     db.refresh(db_nota)
#     return db_nota


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


def update_discipline(db: Session, disciplina: schemas.Disciplina):
    # get the existing data
    db_discipline = db.query(disciplina).filter(
        disciplina.nome == user.id).one_or_none()
    if db_discipline is None:
        return None

    # Update model class variable from requested fields
    for var, value in vars(user).items():
        setattr(db_discipline, var, value) if value else None

    db_discipline.modified = modified_now
    db.add(db_discipline)
    db.commit()
    db.refresh(db_discipline)
    return db_discipline
