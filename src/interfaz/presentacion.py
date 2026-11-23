"""Formato para mostrar (frontera de la interfaz).

Solo ordena en líneas y bloques lo que devuelve el controlador y marca con una clase de color cada parte de la
anotación. No calcula ni decide nada: las métricas (GC, composición, features) no se calculan acá porque no son
parte de HU-04.
"""
import re

ANCHO_LINEA, BLOQUE, MAX_LINEAS = 60, 10, 8
_CALIFICADOR = re.compile(r"^(\s+)(/[\w-]+)(=?)(.*)$")
_CLAVE = re.compile(r"^( {5})(\S+)(\s+)(.*)$")


def _colorear(linea: str) -> list[tuple[str, str]]:
    """Parte una línea de la anotación en trozos con su clase de color (solo para mostrar)."""
    if linea.startswith("FEATURES"):
        return [("h", linea)]
    m = _CALIFICADOR.match(linea)
    if m:
        espacio, nombre, igual, valor = m.groups()
        return [("sp", espacio), ("q", nombre), ("sp", igual), ("v", valor)]
    m = _CLAVE.match(linea)
    if m:
        sangria, clave, espacio, ubicacion = m.groups()
        return [("sp", sangria), ("k", clave), ("sp", espacio), ("loc", ubicacion)]
    return [("v", linea)]


def vista_de_referencia(referencia) -> dict:
    secuencia, anotacion = referencia.secuencia, referencia.anotacion
    mostrada = secuencia[:ANCHO_LINEA * MAX_LINEAS]
    lineas = []
    for inicio in range(0, len(mostrada), ANCHO_LINEA):
        trozo = mostrada[inicio:inicio + ANCHO_LINEA]
        lineas.append((inicio + 1, [trozo[i:i + BLOQUE] for i in range(0, len(trozo), BLOQUE)]))
    return {
        "longitud": len(secuencia),
        "lineas": lineas,
        "mostrada": mostrada,  # el mismo texto del visor, para lectores de pantalla
        "truncada": len(mostrada) < len(secuencia),
        "anotacion": anotacion,
        "anotacion_lineas": [_colorear(linea) for linea in anotacion.splitlines()],
    }
