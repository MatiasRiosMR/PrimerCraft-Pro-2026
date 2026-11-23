"""Adaptador NCBI Entrez: el unico que conoce NCBI. Lee solo lo que necesita (EC-04).

Componente del TP3: Adaptador NCBI Entrez. Contenedor: Preparación de datos (etapa 1). Capa hexagonal: adaptador de salida.

El transporte (como se consigue la respuesta cruda) es intercambiable:
  consultar_entrez    -> consulta real a NCBI
  consultar_grabacion -> respuestas grabadas de NCBI, para trabajar sin internet
"""
import re
import time
from pathlib import Path

from src.aplicacion.puertos import DatosDeReferencia, PuertoReferenciaGenomica, TargetNoEncontrado

EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
# Sintaxis que NCBI admite en una busqueda por codigo de acceso y por organismo. Lo demas (por ejemplo
# "BRCA1 OR TP53") cambiaria la busqueda, asi que se trata como un target que no existe.
IDENTIFICADOR_VALIDO = re.compile(r"[A-Za-z0-9_.]+")
ORGANISMO_VALIDO = re.compile(r"[A-Za-z0-9 .()_/'-]+")
GRABACIONES = Path(__file__).parent / "grabaciones"


def consultar_entrez(identificador: str, organismo: str) -> dict:
    import requests

    comun = {"db": "nuccore", "tool": "primercraft-pro"}
    busqueda = requests.get(
        f"{EUTILS}/esearch.fcgi",
        params={**comun, "retmode": "json",
                "term": f"{identificador}[Accession] AND {organismo}[Organism]"},
        timeout=15,
    )
    busqueda.raise_for_status()
    resultado = busqueda.json().get("esearchresult", {})
    if "idlist" not in resultado:  # NCBI contestó otra cosa (un error): no es lo mismo que «sin resultados»
        raise RuntimeError("respuesta inesperada de NCBI Entrez: no trae la lista de resultados")
    ids = resultado["idlist"]
    if not ids:
        raise TargetNoEncontrado(identificador)
    respuesta = {}
    for clave, tipo in (("fasta", "fasta"), ("genbank", "gb")):
        time.sleep(0.4)  # NCBI admite 3 pedidos por segundo sin clave
        r = requests.get(
            f"{EUTILS}/efetch.fcgi",
            params={**comun, "id": ids[0], "rettype": tipo, "retmode": "text"},
            timeout=15,
        )
        r.raise_for_status()
        respuesta[clave] = r.text
    return respuesta


def consultar_grabacion(identificador: str, organismo: str) -> dict:
    if identificador == "NM_000518" and organismo.strip().lower() == "homo sapiens":
        return {
            "fasta": (GRABACIONES / "NM_000518.fasta").read_text(encoding="utf-8"),
            "genbank": (GRABACIONES / "NM_000518.gb").read_text(encoding="utf-8"),
        }
    if identificador == "NM_SIN_SECUENCIA":  # registro que existe pero viene vacío
        return {"fasta": ">NM_SIN_SECUENCIA.1 registro sin secuencia\n", "genbank": ""}
    raise TargetNoEncontrado(identificador)


class AdaptadorNcbiEntrez(PuertoReferenciaGenomica):
    def __init__(self, transporte=consultar_entrez) -> None:
        self._transporte = transporte

    def obtener_referencia(self, identificador: str, organismo: str) -> DatosDeReferencia:
        identificador, organismo = identificador.strip(), organismo.strip()
        if not (IDENTIFICADOR_VALIDO.fullmatch(identificador) and ORGANISMO_VALIDO.fullmatch(organismo)):
            raise TargetNoEncontrado(identificador)
        return self._leer_campos_conocidos(self._transporte(identificador, organismo))

    def _leer_campos_conocidos(self, respuesta: dict) -> DatosDeReferencia:
        """Toma la secuencia y la anotacion; ignora cualquier otro campo (EC-04)."""
        secuencia = []
        registros = 0
        for linea in respuesta.get("fasta", "").splitlines():
            if linea.startswith(">"):  # la cabecera puede traer cualquier texto
                registros += 1
                if registros > 1:
                    break
            else:
                secuencia.append(linea.strip())
        features, dentro = [], False
        for linea in respuesta.get("genbank", "").splitlines():
            if linea.startswith("FEATURES"):
                dentro = True
            elif linea.startswith("ORIGIN"):
                break
            if dentro:
                features.append(linea)
        return DatosDeReferencia("".join(secuencia), "\n".join(features))
