"""PublicadorDeEtapa: publica los avisos en corrida.estado (simulado en memoria).

Componente del TP3: Publicador de etapa. Contenedor: Preparación de datos (etapa 1).
Capa hexagonal: adaptador de salida. NATS iría detrás de PuertoMensajes.
"""
from src.aplicacion.puertos import Aviso, PuertoMensajes


class PublicadorDeEtapa(PuertoMensajes):
    """Simulado: guarda los avisos en memoria en lugar de publicarlos en NATS."""

    def __init__(self) -> None:
        self.avisos: list[tuple[str, Aviso]] = []

    def publicar_aviso(self, corrida_id: str, aviso: Aviso) -> None:
        self.avisos.append((corrida_id, aviso))
