"""Casos de prueba de HU-04: criterios de aceptación (CP-01 a CP-03), escenarios de calidad (CP-04, CP-05)
y persistencia (CP-06 a CP-08). La tabla completa está en docs/design/diseno-detallado.md (sección 7)."""
import sqlite3

from src.aplicacion.controlador_obtencion_referencia import ControladorObtencionReferencia
from src.aplicacion.gestion_de_excepciones import GestionDeExcepciones
from src.aplicacion.puertos import DatosDeReferencia, PuertoReferenciaGenomica, TargetNoEncontrado
from src.infraestructura.adaptador_ncbi_entrez import AdaptadorNcbiEntrez
from src.infraestructura.publicador_de_etapa import PublicadorDeEtapa
from src.infraestructura.repositorio_referencias import (
    RepositorioReferenciasEnMemoria,
    RepositorioReferenciasSqlite,
)


class ReferenciasFalsas(PuertoReferenciaGenomica):
    """Adaptador falso: devuelve datos fijos o lanza un error."""

    def __init__(self, datos=None, error=None):
        self.datos, self.error = datos, error

    def obtener_referencia(self, identificador, organismo):
        if self.error:
            raise self.error
        return self.datos


def armar(referencias, repositorio=None):
    publicador = PublicadorDeEtapa()
    repositorio = repositorio or RepositorioReferenciasEnMemoria()
    controlador = ControladorObtencionReferencia(
        referencias, GestionDeExcepciones(), publicador, repositorio
    )
    return controlador, publicador, repositorio


def test_cp01_obtiene_la_referencia_cuando_ncbi_la_devuelve():
    controlador, publicador, _ = armar(ReferenciasFalsas(DatosDeReferencia("ACGT", "FEATURES")))
    r = controlador.obtener("c1", "NM_1", "Homo sapiens")
    assert r.obtenida and r.referencia.secuencia == "ACGT" and r.referencia.anotacion == "FEATURES"
    assert publicador.avisos == []


def test_cp02_rechaza_y_avisa_si_el_identificador_no_existe():
    controlador, publicador, _ = armar(ReferenciasFalsas(error=TargetNoEncontrado("NM_X")))
    r = controlador.obtener("c1", "NM_X", "Homo sapiens")
    assert not r.obtenida and r.referencia is None
    assert r.aviso.codigo == "TARGET_NO_ENCONTRADO" and r.aviso.reintentable is False
    assert "NM_X" in r.aviso.mensaje and "Verificá el identificador" in r.aviso.mensaje
    assert publicador.avisos == [("c1", r.aviso)]


def test_cp03_rechaza_si_la_respuesta_no_trae_secuencia():
    controlador, publicador, _ = armar(ReferenciasFalsas(DatosDeReferencia("", "")))
    r = controlador.obtener("c1", "NM_1", "Homo sapiens")
    assert not r.obtenida and r.referencia is None
    assert r.aviso.codigo == "TARGET_NO_ENCONTRADO" and r.aviso.reintentable is False
    assert len(publicador.avisos) == 1


def test_cp04_el_adaptador_ignora_campos_y_cabecera_desconocidos():  # EC-04
    respuesta = {
        "fasta": ">NM_1.9 |campo_nuevo=xyz| otra cabecera\nACGT\nacgt\n",
        "genbank": "LOCUS x\nFEATURES  Location\n  gene 1..8\nORIGIN\n  1 acgt\n",
        "metadatos_nuevos": {"version": 2},
    }
    datos = AdaptadorNcbiEntrez(lambda i, o: respuesta).obtener_referencia("NM_1", "Homo sapiens")
    assert datos.secuencia == "ACGTacgt"
    assert datos.anotacion.startswith("FEATURES") and "ORIGIN" not in datos.anotacion


def test_cp05_el_controlador_funciona_con_otro_proveedor_sin_modificarse():  # EC-03
    class OtroProveedor(PuertoReferenciaGenomica):
        def obtener_referencia(self, identificador, organismo):
            return DatosDeReferencia("TTGGCCAA", "")

    controlador, _, _ = armar(OtroProveedor())
    assert controlador.obtener("c1", "ENSG_1", "Homo sapiens").obtenida


def test_cp06_guarda_la_referencia_cuando_se_obtiene():
    controlador, _, repositorio = armar(ReferenciasFalsas(DatosDeReferencia("ACGT", "")))
    controlador.obtener("c1", "NM_1", "Homo sapiens")
    assert [(c, i, o) for c, i, o, _ in repositorio.guardadas] == [("c1", "NM_1", "Homo sapiens")]


def test_cp07_no_guarda_nada_si_se_rechaza():
    controlador, _, repositorio = armar(ReferenciasFalsas(error=TargetNoEncontrado("NM_X")))
    controlador.obtener("c1", "NM_X", "Homo sapiens")
    assert repositorio.guardadas == []


def test_cp08_sqlite_conserva_la_referencia_al_reabrir_la_base(tmp_path):
    ruta = str(tmp_path / "referencias.db")
    controlador, _, _ = armar(
        ReferenciasFalsas(DatosDeReferencia("ACGT", "FEATURES")), RepositorioReferenciasSqlite(ruta)
    )
    controlador.obtener("c1", "NM_1", "Homo sapiens")
    with sqlite3.connect(ruta) as base:
        filas = base.execute(
            "SELECT corrida_id, identificador, organismo, secuencia, anotacion FROM referencias"
        ).fetchall()
    assert filas == [("c1", "NM_1", "Homo sapiens", "ACGT", "FEATURES")]
