import json
from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import Optional, List

class Discipline(BaseModel):
    nome: str
    nome_professor: Optional[str] = None
    sobrenome_professor: Optional[str] = None
    nota: List[str] = None

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
        json.dump(data, file)

def write_all_file(content):
    with open(filename, "w") as file:
        json.dump(content, file)

@app.get("/")
def read_root():
    return {"Conteudo": "Aplicação de Megadados", "Alunos": "Eiki, João e William"}

@app.get("/disciplines")
def read_disciplines():
    return read_file()

@app.get("/disciplines/names")
def read_disciplines():
    data = read_file()
    lista = []
    for k, v in data.items():
        for k2, v2 in v.items():
            if k2 == "nome":
                lista.append(v2)
    return lista

@app.post("/disciplines")
def create_discipline(new_discipline: Discipline):
    write_file(new_discipline.dict())
    return new_discipline.dict()

@app.delete("/disciplines/{nome}")
def delete_discipline(nome: str):
    data = read_file()
    data.pop(nome)
    write_all_file(data)
    return data

@app.get("/disciplines/notes/{nome}")
def read_notes_from_discipline(nome: str):
    data = read_file()
    lista = []
    for k, v in data.items():
        if k == nome:
            for k2, v2 in v.items():
                if k2 == "nota":
                    for i in v2:
                        lista.append(i['descricao'])
    if len(lista) == 0:
        return {"Message": "Essa disciplina não tem notas"}
    return lista

# @app.delete("/disciplines/notes/{nome}")
# def delete_note(nome: str):
#     data = read_file()
#     data_discipline = data[nome]
#     print(data_discipline)
#     # data.pop(nome)
#     # write_all_file(data)
#     # return data

# data = [
#     {
#         "name": "name_discipline",
#         "professor": "Neymar",
#         "description": "Essa disciplina eh top"
#     },
#     {
#         "name": "another",
#         "professor": "Roger Guedes",
#         "description": "Essa eh mais top"
#     }
# ]