"""ConsumidorDeEtapa: recibe corrida.solicitada y confirma el mensaje después de publicar (DA-02).

Componente del TP3: Consumidor de etapa. Contenedor: Preparación de datos (etapa 1).
Capa hexagonal: adaptador de entrada. Simula la tubería de NATS.
"""
from src.aplicacion.controlador_obtencion_referencia import (
    ControladorObtencionReferencia,
    Resultado,
)


class ConsumidorDeEtapa:
    """Adaptador de entrada de la tuberia corrida.solicitada (simulada)."""

    def __init__(self, controlador: ControladorObtencionReferencia) -> None:
        self._controlador = controlador
        self.confirmados: list[str] = []

    def procesar(self, mensaje: dict) -> Resultado:
        """Traduce el JSON de corrida.solicitada (TP3, sección 5.2) a la llamada al controlador."""
        carga = mensaje["carga"]
        resultado = self._controlador.obtener(
            mensaje["idCorrida"], carga["identificadorNcbi"], carga["organismo"]
        )
        if not resultado.obtenida:
            # El aviso ya se publicó: recién ahora se confirma el mensaje (DA-02).
            # En el éxito confirma la etapa tras publicar referencia.localizada (HU-02.1).
            self.confirmar(mensaje)
        return resultado

    def confirmar(self, mensaje: dict) -> None:
        self.confirmados.append(mensaje["idCorrida"])
