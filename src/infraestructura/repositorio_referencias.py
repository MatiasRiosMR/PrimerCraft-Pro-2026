"""Persistencia de las referencias obtenidas, detras de RepositorioReferencias.

Sin componente en el TP3: excepción a DA-04 (persistencia local de demostración; en el sistema real la guarda
el Servidor de corridas). Capa hexagonal: adaptador de salida.

Dos implementaciones intercambiables: en memoria (pruebas) y SQLite (por defecto).
"""
import sqlite3
import threading
from datetime import datetime, timezone

from src.aplicacion.puertos import RepositorioReferencias
from src.dominio.informacion_genoma import InformacionGenoma


class RepositorioReferenciasEnMemoria(RepositorioReferencias):
    def __init__(self) -> None:
        self.guardadas: list[tuple[str, str, str, InformacionGenoma]] = []

    def guardar(self, corrida_id: str, identificador: str, organismo: str,
                referencia: InformacionGenoma) -> None:
        self.guardadas.append((corrida_id, identificador, organismo, referencia))


class RepositorioReferenciasSqlite(RepositorioReferencias):
    def __init__(self, ruta: str = "primercraft.db") -> None:
        self._conexion = sqlite3.connect(ruta, check_same_thread=False)
        self._cerrojo = threading.Lock()
        with self._conexion:
            self._conexion.execute(
                "CREATE TABLE IF NOT EXISTS referencias ("
                "corrida_id TEXT PRIMARY KEY, identificador TEXT NOT NULL, organismo TEXT NOT NULL, "
                "secuencia TEXT NOT NULL, anotacion TEXT NOT NULL, fecha TEXT NOT NULL)"
            )

    def guardar(self, corrida_id: str, identificador: str, organismo: str,
                referencia: InformacionGenoma) -> None:
        with self._cerrojo, self._conexion:
            self._conexion.execute(
                "INSERT OR REPLACE INTO referencias VALUES (?, ?, ?, ?, ?, ?)",
                (corrida_id, identificador, organismo, referencia.secuencia,
                 referencia.anotacion, datetime.now(timezone.utc).isoformat()),
            )
