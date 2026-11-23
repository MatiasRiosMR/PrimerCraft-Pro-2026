"""Interfaz grafica (boundary). Solo conoce al controlador: no calcula ni tiene reglas de negocio.

Representa la frontera hacia la persona. En el TP3 esa pieza es la Aplicación web (React, MVVM) y habla con el
Servidor de corridas; en esta demostración de HU-04 es una pantalla mínima que llama directo al controlador.
El formato de lo que se muestra está en presentacion.py.
"""
import logging
import uuid
from pathlib import Path

from fastapi import FastAPI, Form, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.arranque import MODO, armar_controlador
from src.interfaz.presentacion import vista_de_referencia

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
registro = logging.getLogger("primercraft")

AQUI = Path(__file__).parent
app = FastAPI(title="PrimerCraft Pro · HU-04")
app.mount("/static", StaticFiles(directory=str(AQUI / "static")), name="static")
plantillas = Jinja2Templates(directory=str(AQUI / "templates"))
controlador = armar_controlador()


def _pantalla(request: Request, identificador: str, organismo: str, **extra):
    contexto = {"identificador": identificador, "organismo": organismo, "modo": MODO, **extra}
    return plantillas.TemplateResponse(request, "pantalla.html", contexto)


@app.get("/")
def formulario(request: Request):
    return _pantalla(request, "NM_000518", "Homo sapiens")


@app.post("/")
def consultar(request: Request, identificador: str = Form(...), organismo: str = Form(...)):
    try:
        resultado = controlador.obtener(uuid.uuid4().hex, identificador, organismo)
    except Exception:  # falla inesperada (p. ej. sin conexion): el reintento (DA-03) queda fuera de HU-04
        registro.exception("Falla inesperada al obtener la referencia de %r", identificador)
        return _pantalla(request, identificador, organismo, falla=True)
    vista = vista_de_referencia(resultado.referencia) if resultado.obtenida else None
    return _pantalla(request, identificador, organismo, resultado=resultado, vista=vista)
