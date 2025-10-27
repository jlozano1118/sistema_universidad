from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session
from typing import List
from utils.db import engine, crear_db, get_session
from data.models import Estudiante,Curso,Matricula

from operations.operations import (crear_estudiante,
                                   listar_estudiantes_por_semestre,
                                   actualizar_estudiante,
                                   eliminar_estudiante,
                                   crear_curso)

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

@app.get("/estudiantes/", response_model=List[Estudiante], summary="Listar estudiantes por semestre")
def obtener_estudiantes_por_semestre(semestre: int, session: Session = Depends(get_session)):
    return listar_estudiantes_por_semestre(session, semestre)


@app.put("/estudiantes/{cedula}")
def actualizar_estudiantes(cedula: str, datos: Estudiante, session: Session = Depends(get_session)):
    return actualizar_estudiante(session, cedula, datos)

@app.delete("/estudiantes/{cedula}", summary="Eliminar un estudiante")
def eliminar_estudiantes(cedula: str, session: Session = Depends(get_session)):
    return eliminar_estudiante(session, cedula)

@app.post("/cursos/", response_model=Curso, summary="Crear un nuevo curso")
def crear_nuevo_curso(curso: Curso, session: Session = Depends(get_session)):
    return crear_curso(session, curso)