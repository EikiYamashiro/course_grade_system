from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/disciplines/names", status_code=200)
def read_all_disciplines(db: Session = Depends(get_db)):
    db_discipline = crud.get_name_disciplinas(db)
    print(db_discipline)
    return db_discipline


@app.post("/disciplines", status_code=201, response_model=schemas.Disciplina)
def create_discipline(new_discipline: schemas.Disciplina, db: Session = Depends(get_db)):
    db_discipline = crud.get_disciplina(db, nome=new_discipline.nome)
    # A disciplina tem um nome único (obrigatório)
    if db_discipline:
        raise HTTPException(status_code=400, detail="Disciplina já existente")
    return crud.create_discipline(db=db, disciplina=new_discipline)


@app.delete("/disciplines/{nome}")
def delete_discipline(nome: str, db: Session = Depends(get_db)):
    db_discipline = crud.get_disciplina(db, nome=nome)
    if db_discipline:
        return crud.delete_discipline(db=db, nome=nome)
    raise HTTPException(status_code=404, detail="Disciplina não encontrada")


@app.put("/disciplines/{nome}", status_code=200)
def update_discipline(nome: str, disciplina: Discipline):
    db_discipline = crud.get_disciplina(db, nome=nome)
    if db_discipline:
        return crud.update_discipline(db=db, disciplina=disciplina)
    raise HTTPException(status_code=404, detail="Disciplina não encontrada")

    data = read_file()
    dictionary = {}
    if see_if_exists(data, nome):
        for k, v in data.items():
            notas = False
            nome_professor = False
            sobrenome_professor = False
            for i in v:
                if i == "notas":
                    notas = True
                if i == "nome_professor":
                    nome_professor = True
                if i == "sobrenome_professor":
                    sobrenome_professor = True
            if k == nome:
                dictionary['nome'] = disciplina.nome
                if nome_professor:
                    dictionary['nome_professor'] = disciplina.nome_professor
                if sobrenome_professor:
                    dictionary['sobrenome_professor'] = disciplina.sobrenome_professor
                if notas:
                    dictionary['notas'] = data[nome]['notas']
        data[disciplina.nome] = dictionary
    else:
        raise HTTPException(
            status_code=404, detail="Disciplina não encontrada")
    if not disciplina.nome == nome:
        del data[nome]
    write_all_file(data)
    return {"Detail": "Disciplina alterada com sucesso"}


# @app.post("/users/", response_model=schemas.User)
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     db_user = crud.get_user_by_email(db, email=user.email)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     return crud.create_user(db=db, user=user)


# @app.get("/users/", response_model=List[schemas.User])
# def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     users = crud.get_users(db, skip=skip, limit=limit)
#     return users


# @app.get("/users/{user_id}", response_model=schemas.User)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud.get_user(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user


# @app.post("/users/{user_id}/items/", response_model=schemas.Item)
# def create_item_for_user(
#     user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
# ):
#     return crud.create_user_item(db=db, item=item, user_id=user_id)


# @app.get("/items/", response_model=List[schemas.Item])
# def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     items = crud.get_items(db, skip=skip, limit=limit)
#     return items
