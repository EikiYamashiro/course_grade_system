import json
from fastapi import FastAPI, Query
from fastapi.param_functions import Body
from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID

class Nota(BaseModel):
    id: UUID
    descricao: str

# A disciplina tem um nome de professor (opcional)
# A disciplina tem um campo de anotação livre (texto)
class Discipline(BaseModel):
    nome: str
    nome_professor: Optional[str] = None
    sobrenome_professor: Optional[str] = None

app = FastAPI()
filename = "disciplines.json"

def read_file():
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

def write_file(content):
    data = read_file()
    data[content["nome"]] = content
    with open(filename, "w") as file:
        json.dump(data, file, ensure_ascii=True, indent=4, sort_keys=True)

def write_all_file(content):
    with open(filename, "w") as file:
        json.dump(content, file, ensure_ascii=True, indent=4, sort_keys=True)

def see_if_exists(data, disciplina):
    for i in data:
        if i == disciplina:
            return True
    return False


@app.get("/")
def read_root():
    return {"Conteudo": "Aplicação de Megadados", "Alunos": "Eiki, João e William"}


# O usuário pode listar os nomes de suas disciplinas
@app.get("/disciplines/names")
def read_name_disciplines():
    data = read_file()
    lista = []
    for k, v in data.items():
        for k2, v2 in v.items():
            if k2 == "nome":
                lista.append(v2)
    return lista


# O usuário pode criar uma disciplina
@app.post("/disciplines")
def create_discipline(new_discipline: Discipline):
    data = read_file()
    disciplines = list(data.keys())
    # A disciplina tem um nome único (obrigatório)
    if new_discipline.nome not in disciplines:
        write_file(new_discipline.dict())
        return new_discipline.dict()
    return {"Error": "Disciplina já existente"}


# O usuário pode deletar uma disciplina
@app.delete("/disciplines/{nome}")
def delete_discipline(nome: str):
    data = read_file()
    if see_if_exists(data, nome):
        data.pop(nome)
        write_all_file(data)
        return data
    return {"Error": "Disciplina não existente"}


# O usuário pode listar as notas de uma disciplina
@app.get("/disciplines/notes/{nome}")
def read_notes_from_discipline(nome: str):
    data = read_file()
    dictionary = {}
    for k, v in data.items():
        if k == nome:
            for k2, v2 in v.items():
                if k2 == "notas":
                    for i in v2:
                        dictionary[i['id']] = i['descricao']
    if len(dictionary) == 0:
        return {"Error": "Essa disciplina não tem notas"}
    return dictionary


# O usuário pode adicionar uma nota a uma disciplina
@app.post("/disciplines/{disciplina}")
def create_discipline_note(disciplina: str, nota: Nota):
    data = read_file()
    already_exists = False
    if see_if_exists(data, disciplina):
        data_discipline = data[disciplina]
        nota.id = str(nota.id)
        for i in data_discipline['notas']:
            if i['id'] == nota.id:
                already_exists = True
        if not already_exists:
            data_discipline['notas'].append(nota.dict())
            data[disciplina] = data_discipline
            write_all_file(data)
            return data_discipline
        return {"Error": "Uma nota com esse identificador já existe"}
    else:
        return {"Error": "Disciplina não existente"}


# O usuário pode deletar uma nota de uma disciplina
@app.delete("/disciplines/{nome}/notes/{id}")
def delete_note_from_discipline(nome: str, id: int):
    data = read_file()
    if see_if_exists(data, nome):
        data_discipline = data[nome]
        exists = False
        for i in data_discipline["notas"]:
            if int(i['id']) == id:
                index = data_discipline["notas"].index(i)
                del data_discipline["notas"][index]
                exists = True
        if exists:
            data[nome] = data_discipline
            write_all_file(data)
            return data_discipline
        return {"Error": "Essa anotação não existe"}
    return {"Error": "Disciplina não existente"}


# O usuário pode modificar uma nota de uma disciplina
@app.put("/disciplines/{disciplina}/notes/")
def update_note(disciplina: str, nota: Nota = Body(..., description="Remember to put the correct ID")):
    data = read_file()
    if see_if_exists(data, disciplina):
        data_discipline = data[disciplina]
        exists = False
        for i in data_discipline["notas"]:
            if int(i['id']) == int(nota.id):
                i['descricao'] = nota.descricao
                exists = True
        if exists:
            data[disciplina] = data_discipline
            write_all_file(data)
            return {"Anotação alterada com sucesso"}
        return {"Error": "Essa anotação não existe"}
    return {"Error": "Disciplina não existente"}

'''
CHECK O usuário pode criar uma disciplina
CHECK A disciplina tem um nome único (obrigatório)
CHECK A disciplina tem um nome de professor (opcional)
CHECK A disciplina tem um campo de anotação livre (texto)
CHECK O usuário pode deletar uma disciplina
CHECK O usuário pode listar os nomes de suas disciplinas
• O usuário pode modificar as informações de uma disciplina INCLUINDO seu nome
CHECK O usuário pode adicionar uma nota a uma disciplina
CHECK O usuário pode deletar uma nota de uma disciplina
CHECK O usuário pode listar as notas de uma disciplina
CHECK O usuário pode modificar uma nota de uma disciplina
'''