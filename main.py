from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session
from typing import List
from utils.db import engine, crear_db, get_session
from data.models import Estudiante,Curso,Matricula

from operations.operations import (crear_estudiante)

app = FastAPI(
    title="API de Sistema de Gestion de Universidad",
    description="API para Estudiantes, Cursos y Matriculas",
)

@app.get("/")
def root():
    return {"mensaje": "Bienvenido a la API de Sistema de Gestion de Universidad"}

@app.on_event("startup")
def startup():
    crear_db()

@app.post("/estudiantes/", response_model=Estudiante, summary="Crear un nuevo estudiante")
def crear_nuevo_estudiante(estudiante: Estudiante, session: Session = Depends(get_session)):
    return crear_estudiante(session, estudiante)

