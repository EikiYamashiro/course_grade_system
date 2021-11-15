from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import SessionLocal, engine

try:
    models.Base.metadata.create_all(bind=engine)
except:
    print("Base de dados já existente")

app = FastAPI()

# Dependency


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Conteudo": "Aplicação de Megadados", "Alunos": "Eiki, João e William"}


@app.post("/disciplines", status_code=201, response_model=schemas.Disciplina)
def create_discipline(new_discipline: schemas.Disciplina, db: Session = Depends(get_db)):
    db_discipline = crud.get_disciplina(db, nome=new_discipline.nome)
    # A disciplina tem um nome único (obrigatório)
    if db_discipline:
        raise HTTPException(status_code=400, detail="Disciplina já existente")
    return crud.create_discipline(db=db, disciplina=new_discipline)


# O usuário pode listar os nomes de suas disciplinas
@app.get("/disciplines/names", status_code=200)
def read_all_disciplines(db: Session = Depends(get_db)):
    lista = []
    db_discipline = crud.get_name_disciplinas(db)
    for item in db_discipline:
        lista.append(item.nome)
    return lista


# O usuário pode modificar as informações de uma disciplina INCLUINDO seu nome
@app.put("/disciplines/{nome}", status_code=200)
def update_discipline(nome: str, disciplina: schemas.Disciplina, db: Session = Depends(get_db)):
    db_discipline = crud.get_disciplina(db, nome=nome)
    if db_discipline:
        return crud.update_discipline(db=db, disciplina=disciplina, nome=nome)
    raise HTTPException(status_code=404, detail="Disciplina não encontrada")


# O usuário pode deletar uma disciplina
@app.delete("/disciplines/{nome}")
def delete_discipline(nome: str, db: Session = Depends(get_db)):
    db_discipline = crud.get_disciplina(db, nome=nome)
    if db_discipline:
        return crud.delete_discipline(db=db, nome=nome)
    raise HTTPException(status_code=404, detail="Disciplina não encontrada")


# O usuário pode adicionar uma nota a uma disciplina
@app.post("/disciplines/{disciplina}", status_code=201)
def create_discipline_note(disciplina: str, nota: schemas.NotaCreate, db: Session = Depends(get_db)):
    db_discipline = crud.get_disciplina(db, nome=disciplina)
    ids = []
    if db_discipline:
        notas = crud.get_index_nota(db, nome=disciplina)
        for n in notas:
            ids.append(n.id)
        if nota.id in ids:
            raise HTTPException(status_code=404, detail="ID já existente")
        return crud.create_nota(db=db, nota=nota, disciplina=disciplina)
    raise HTTPException(status_code=404, detail="Disciplina não encontrada")


# O usuário pode listar as notas de uma disciplina
@app.get("/disciplines/notes/{nome}", status_code=200)
def read_notes_from_discipline(nome: str, db: Session = Depends(get_db)):
    db_discipline = crud.get_disciplina(db, nome=nome)
    if db_discipline:
        return crud.get_notas(db=db, nome=nome)
    raise HTTPException(status_code=404, detail="Disciplina não encontrada")


# O usuário pode deletar uma nota de uma disciplina
@app.delete("/disciplines/{nome}/notes/{id}", status_code=200)
def delete_note_from_discipline(nome: str, id: int, db: Session = Depends(get_db)):
    db_discipline = crud.get_disciplina(db, nome=nome)
    if db_discipline:
        if crud.delete_nota(db=db, nome=nome, id=id):
            return {"Detail": "Nota deletada com sucesso"}
        raise HTTPException(status_code=404, detail="Nota não encontrada")
    raise HTTPException(status_code=404, detail="Disciplina não encontrada")


# O usuário pode modificar uma nota de uma disciplina
@app.put("/disciplines/{disciplina}/notes/{id}", status_code=201)
def update_note(disciplina: str, id: int, nota: schemas.NotaCreate, db: Session = Depends(get_db)):
    db_discipline = crud.get_disciplina(db, nome=disciplina)
    ids = []
    if db_discipline:
        notas = crud.get_index_nota(db, nome=disciplina)
        for n in notas:
            ids.append(n.id)
        if id in ids:
            if nota.id != id:
                raise HTTPException(
                    status_code=404, detail="O ID não pode ser alterado")
            else:
                return crud.update_nota(db=db, nota=nota, nome=disciplina)
        raise HTTPException(status_code=404, detail="Nota não existente")
    raise HTTPException(status_code=404, detail="Disciplina não encontrada")
