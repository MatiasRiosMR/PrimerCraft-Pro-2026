"""Punto de arranque: el unico lugar donde se arman los objetos concretos.

Arma el contenedor Preparación de datos (etapa 1) del TP3: cablea el controlador con el adaptador, la gestión
de excepciones, el publicador y el repositorio.

Variables de entorno:
  PRIMERCRAFT_NCBI  real (por defecto: consulta NCBI por internet) o simulado (respuestas grabadas)
  PRIMERCRAFT_DB    archivo SQLite donde se guardan las referencias (por defecto primercraft.db)
"""
import os

from src.aplicacion.controlador_obtencion_referencia import ControladorObtencionReferencia
from src.aplicacion.gestion_de_excepciones import GestionDeExcepciones
from src.infraestructura.adaptador_ncbi_entrez import (
    AdaptadorNcbiEntrez,
    consultar_entrez,
    consultar_grabacion,
)
from src.infraestructura.publicador_de_etapa import PublicadorDeEtapa
from src.infraestructura.repositorio_referencias import RepositorioReferenciasSqlite

MODO = "simulado" if os.environ.get("PRIMERCRAFT_NCBI") == "simulado" else "real"
RUTA_BD = os.environ.get("PRIMERCRAFT_DB", "primercraft.db")


def armar_controlador(modo: str = MODO, ruta_bd: str = RUTA_BD) -> ControladorObtencionReferencia:
    transporte = consultar_grabacion if modo == "simulado" else consultar_entrez
    return ControladorObtencionReferencia(
        AdaptadorNcbiEntrez(transporte),
        GestionDeExcepciones(),
        PublicadorDeEtapa(),
        RepositorioReferenciasSqlite(ruta_bd),
    )
