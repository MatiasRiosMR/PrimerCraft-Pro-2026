"""ControladorObtencionReferencia y Resultado.

Componente del TP3: Obtención de referencia. Contenedor: Preparación de datos (etapa 1).
Capa hexagonal: núcleo. Orquesta la HU-04 y solo conoce interfaces (puertos).
"""
from dataclasses import dataclass
from typing import Optional

from src.aplicacion.gestion_de_excepciones import GestionDeExcepciones
from src.aplicacion.puertos import (
    Aviso,
    PuertoMensajes,
    PuertoReferenciaGenomica,
    RepositorioReferencias,
)
from src.dominio.informacion_genoma import InformacionGenoma


@dataclass(frozen=True)
class Resultado:
    obtenida: bool
    referencia: Optional[InformacionGenoma] = None
    aviso: Optional[Aviso] = None


class ControladorObtencionReferencia:
    def __init__(
        self,
        referencias: PuertoReferenciaGenomica,
        excepciones: GestionDeExcepciones,
        mensajes: PuertoMensajes,
        repositorio: RepositorioReferencias,
    ) -> None:
        self._referencias = referencias
        self._excepciones = excepciones
        self._mensajes = mensajes
        self._repositorio = repositorio

    def obtener(self, corrida_id: str, identificador: str, organismo: str) -> Resultado:
        try:
            datos = self._referencias.obtener_referencia(identificador, organismo)
            referencia = InformacionGenoma(datos.secuencia, datos.anotacion)
        except Exception as error:
            aviso = self._excepciones.clasificar(error, identificador)
            self._mensajes.publicar_aviso(corrida_id, aviso)
            return Resultado(False, aviso=aviso)
        self._repositorio.guardar(corrida_id, identificador, organismo, referencia)
        return Resultado(True, referencia=referencia)
