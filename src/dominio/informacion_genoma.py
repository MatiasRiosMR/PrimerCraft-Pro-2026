"""Entidad InformacionGenoma.

Regla: una referencia solo es valida si trae una secuencia no vacia con alfabeto IUPAC.
La anotacion es opcional (EC-01 prevé genomas sin anotacion).

Componente del TP3: Obtención de referencia (las entidades viven en el núcleo, no son un componente aparte).
Contenedor: Preparación de datos (etapa 1). Capa hexagonal: núcleo.
"""

ALFABETO_IUPAC = frozenset("ACGTURYSWKMBDHVN")


class ReferenciaSinSecuencia(Exception):
    pass


class InformacionGenoma:
    def __init__(self, secuencia: str, anotacion: str = "") -> None:
        limpia = "".join(secuencia.split()).upper()
        if not limpia:
            raise ReferenciaSinSecuencia("la referencia no trae secuencia")
        invalidos = sorted(set(limpia) - ALFABETO_IUPAC)
        if invalidos:
            raise ReferenciaSinSecuencia("caracteres fuera de IUPAC: " + ", ".join(invalidos))
        self.secuencia = limpia
        self.anotacion = anotacion
