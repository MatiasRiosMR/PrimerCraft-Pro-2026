"""GestionDeExcepciones: decide si un error es definitivo o pasajero y arma el aviso (DA-03).

Componente del TP3: Gestión de excepciones. Contenedor: Preparación de datos (etapa 1).
Capa hexagonal: núcleo.
"""
from src.aplicacion.puertos import Aviso, TargetNoEncontrado
from src.dominio.informacion_genoma import ReferenciaSinSecuencia


class GestionDeExcepciones:
    def clasificar(self, error: Exception, identificador: str) -> Aviso:
        """Los dos errores de HU-04 son definitivos. Cualquier otro se vuelve a lanzar."""
        if isinstance(error, (TargetNoEncontrado, ReferenciaSinSecuencia)):
            return Aviso(
                "TARGET_NO_ENCONTRADO",
                f"No se encontró el target {identificador}. Verificá el identificador ingresado.",
                reintentable=False,
            )
        raise error
