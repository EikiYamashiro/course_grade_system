import json
from fastapi import FastAPI, HTTPException
from fastapi.param_functions import Body
from pydantic import BaseModel
from typing import Optional
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
@app.get("/disciplines/names", status_code=200)
def read_name_disciplines():
    data = read_file()
    lista = []
    i = 0
    for k, v in data.items():
        for k2, v2 in v.items():
            if k2 == "nome":
                i += 1
                lista.append(i)
                lista.append(v2)
    print("ola")
    return {lista[i]: lista[i + 1] for i in range(0, len(lista), 2)}  # *


# O usuário pode criar uma disciplina
@app.post("/disciplines", status_code=201)
def create_discipline(new_discipline: Discipline):
    data = read_file()
    disciplines = list(data.keys())
    # A disciplina tem um nome único (obrigatório)
    if new_discipline.nome not in disciplines:
        write_file(new_discipline.dict())
        return {"detail": "Disciplina criada com sucesso"}
    raise HTTPException(status_code=400, detail="Disciplina já existente")


# O usuário pode deletar uma disciplina
@app.delete("/disciplines/{nome}")
def delete_discipline(nome: str):
    data = read_file()
    if see_if_exists(data, nome):
        data.pop(nome)
        write_all_file(data)
        return {"Detail": "Disciplina deletada com sucesso"}
    raise HTTPException(status_code=404, detail="Disciplina não encontrada")

# O usuário pode modificar as informações de uma disciplina INCLUINDO seu nome


@app.put("/disciplines/{nome}", status_code=200)
def update_discipline(nome: str, disciplina: Discipline):
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

# O usuário pode listar as notas de uma disciplina


@app.get("/disciplines/notes/{nome}", status_code=200)
def read_notes_from_discipline(nome: str):
    data = read_file()
    if see_if_exists(data, nome):
        dictionary = {}
        for k, v in data.items():
            if k == nome:
                for k2, v2 in v.items():
                    if k2 == "notas":
                        for i in v2:
                            dictionary[i['id']] = i['descricao']
        if len(dictionary) == 0:
            raise HTTPException(
                status_code=400, detail="Essa disciplina não tem notas")
        return dictionary
    raise HTTPException(status_code=404, detail="Disciplina não encontrada")


# O usuário pode adicionar uma nota a uma disciplina
@app.post("/disciplines/{disciplina}", status_code=201)
def create_discipline_note(disciplina: str, nota: Nota):
    data = read_file()
    already_exists = False
    if see_if_exists(data, disciplina):
        data_discipline = data[disciplina]
        nota.id = str(nota.id)
        notas = False
        for k, v in data.items():
            if k == disciplina:
                for i in v:
                    if i == "notas":
                        notas = True
                        for i in data_discipline['notas']:
                            if i['id'] == nota.id:
                                already_exists = True
        if not notas:
            data_discipline['notas'] = []
        if not already_exists:
            data_discipline['notas'].append(nota.dict())
            data[disciplina] = data_discipline
            write_all_file(data)
            return {"Detail": "Nota adicionada com sucesso"}
        raise HTTPException(
            status_code=400, detail="Uma nota com esse id já existe")
    else:
        raise HTTPException(
            status_code=404, detail="Disciplina não encontrada")

# O usuário pode modificar uma nota de uma disciplina


@app.put("/disciplines/{disciplina}/notes/", status_code=201)
def update_note(disciplina: str, nota: Nota = Body(..., description="Remember to put the correct ID")):
    data = read_file()
    if see_if_exists(data, disciplina):
        data_discipline = data[disciplina]
        exists = False
        for i in data_discipline["notas"]:
            if str(i['id']) == str(nota.id):
                i['descricao'] = nota.descricao
                exists = True
        if exists:
            data[disciplina] = data_discipline
            write_all_file(data)
            return {"Detail": "Anotação alterada com sucesso"}
        raise HTTPException(
            status_code=404, detail="Nota não encontrada nessa disciplina")
    raise HTTPException(status_code=404, detail="Disciplina não encontrada")

# O usuário pode deletar uma nota de uma disciplina


@app.delete("/disciplines/{nome}/notes/{id}", status_code=200)
def delete_note_from_discipline(nome: str, id: UUID):
    data = read_file()
    if see_if_exists(data, nome):
        data_discipline = data[nome]
        exists = False
        for i in data_discipline["notas"]:
            if str(i['id']) == str(id):
                index = data_discipline["notas"].index(i)
                del data_discipline["notas"][index]
                exists = True
        if exists:
            data[nome] = data_discipline
            write_all_file(data)
            return {"Detail": "Anotação deletada com sucesso"}
        raise HTTPException(status_code=404, detail="Nota não encontrada")
    raise HTTPException(status_code=404, detail="Disciplina não encontrada")
