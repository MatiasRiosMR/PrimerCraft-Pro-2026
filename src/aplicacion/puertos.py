"""Puertos del nucleo (patron hexagonal) y los tipos que cruzan por ellos.

Componentes del TP3: Puerto de referencia genómica (PuertoReferenciaGenomica) y Puerto de mensajes (PuertoMensajes).
Contenedor: Preparación de datos (etapa 1). Capa hexagonal: núcleo (interfaces).
RepositorioReferencias no tiene componente en el TP3: es la excepción a DA-04 documentada en el diseño (5.2).
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.dominio.informacion_genoma import InformacionGenoma


@dataclass(frozen=True)
class DatosDeReferencia:
    secuencia: str
    anotacion: str


@dataclass(frozen=True)
class Aviso:
    """Aviso para corrida.estado. Mismos campos que `carga` del mensaje (TP3, sección 5.2)."""

    codigo: str  # por ejemplo "TARGET_NO_ENCONTRADO"
    mensaje: str
    reintentable: bool  # False: error definitivo (se informa, no se reintenta)


class TargetNoEncontrado(Exception):
    pass


class PuertoReferenciaGenomica(ABC):
    @abstractmethod
    def obtener_referencia(self, identificador: str, organismo: str) -> DatosDeReferencia:
        """Devuelve secuencia y anotacion. Lanza TargetNoEncontrado si no hay resultados."""


class PuertoMensajes(ABC):
    @abstractmethod
    def publicar_aviso(self, corrida_id: str, aviso: Aviso) -> None:
        """Publica un aviso en corrida.estado."""


class RepositorioReferencias(ABC):
    @abstractmethod
    def guardar(
        self, corrida_id: str, identificador: str, organismo: str, referencia: InformacionGenoma
    ) -> None:
        """Guarda la referencia obtenida para una corrida."""
