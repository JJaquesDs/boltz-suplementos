from fastapi import FastAPI

from sqlmodel import SQLModel

from core.database import engine

app = FastAPI()

@app.on_event
def on_start():
    """ Função para criar todas as tabelas no banco """
    SQLModel.metadata.create_all(engine)

