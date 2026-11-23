"""Casos agregados al revisar la cobertura, el código, la complejidad ciclomática y si las pruebas detectan cambios
en el código (CP-09 a CP-28): entidad, gestión de excepciones, consumidor, adaptador (camino real, registros
múltiples, respuesta vacía, variantes del FASTA) y flujo con las respuestas grabadas de NCBI."""
import pytest

from src.aplicacion.controlador_obtencion_referencia import ControladorObtencionReferencia
from src.aplicacion.gestion_de_excepciones import GestionDeExcepciones
from src.aplicacion.puertos import TargetNoEncontrado
from src.dominio.informacion_genoma import InformacionGenoma, ReferenciaSinSecuencia
from src.infraestructura.adaptador_ncbi_entrez import (
    AdaptadorNcbiEntrez,
    consultar_entrez,
    consultar_grabacion,
)
from src.infraestructura.consumidor_de_etapa import ConsumidorDeEtapa
from src.infraestructura.publicador_de_etapa import PublicadorDeEtapa
from src.infraestructura.repositorio_referencias import RepositorioReferenciasEnMemoria


def controlador_con_grabaciones():
    return ControladorObtencionReferencia(
        AdaptadorNcbiEntrez(consultar_grabacion),
        GestionDeExcepciones(),
        PublicadorDeEtapa(),
        RepositorioReferenciasEnMemoria(),
    )


def mensaje(identificador):
    """Mensaje corrida.solicitada con el formato del TP3 (sección 5.2)."""
    return {
        "version": "1", "idMensaje": "m1", "idCorrida": "c1", "tipoCorrida": "diseno",
        "emisor": "servidor", "fecha": "2026-11-11T12:00:00Z",
        "carga": {"identificadorNcbi": identificador, "organismo": "Homo sapiens"},
    }


def test_cp09_la_entidad_normaliza_la_secuencia():
    assert InformacionGenoma("acg t\nn").secuencia == "ACGTN"


def test_cp10_la_entidad_rechaza_caracteres_fuera_de_iupac():
    with pytest.raises(ReferenciaSinSecuencia):
        InformacionGenoma("ACGT123")


def test_cp11_la_gestion_de_excepciones_no_oculta_errores_desconocidos():
    with pytest.raises(ValueError):
        GestionDeExcepciones().clasificar(ValueError("otro"), "NM_1")


def test_cp12_el_consumidor_traduce_el_json_y_llama_al_controlador():
    resultado = ConsumidorDeEtapa(controlador_con_grabaciones()).procesar(mensaje("NM_000518"))
    assert resultado.obtenida


def test_cp13_el_consumidor_confirma_el_mensaje_despues_de_publicar_el_aviso():
    eventos = []

    class PublicadorQueAnota(PublicadorDeEtapa):
        def publicar_aviso(self, corrida_id, aviso):
            eventos.append("aviso publicado")
            super().publicar_aviso(corrida_id, aviso)

    class ConsumidorQueAnota(ConsumidorDeEtapa):
        def confirmar(self, mensaje):
            eventos.append("mensaje confirmado")
            super().confirmar(mensaje)

    controlador = ControladorObtencionReferencia(
        AdaptadorNcbiEntrez(consultar_grabacion), GestionDeExcepciones(),
        PublicadorQueAnota(), RepositorioReferenciasEnMemoria(),
    )
    consumidor = ConsumidorQueAnota(controlador)
    consumidor.procesar(mensaje("NM_999999"))
    assert eventos == ["aviso publicado", "mensaje confirmado"]
    assert consumidor.confirmados == ["c1"]


def test_cp14_el_consumidor_no_confirma_en_el_exito():
    consumidor = ConsumidorDeEtapa(controlador_con_grabaciones())
    consumidor.procesar(mensaje("NM_000518"))
    assert consumidor.confirmados == []


def test_cp15_el_adaptador_toma_solo_el_primer_registro_del_fasta():
    respuesta = {"fasta": ">uno\nACGT\n>dos\nGGGG\n", "genbank": ""}
    datos = AdaptadorNcbiEntrez(lambda i, o: respuesta).obtener_referencia("NM_1", "Homo sapiens")
    assert datos.secuencia == "ACGT"


class RespuestaFalsa:
    def __init__(self, texto="", json=None):
        self.text, self._json = texto, json or {}

    def raise_for_status(self):
        pass

    def json(self):
        return self._json


def falso_ncbi(monkeypatch, ids, pedidos=None):
    """Reemplaza requests.get por una respuesta de NCBI armada a mano (sin internet ni esperas).
    Si se pasa una lista en `pedidos`, anota en ella los parámetros de cada pedido."""
    monkeypatch.setattr("time.sleep", lambda segundos: None)

    def get(url, params=None, timeout=None):
        if pedidos is not None:
            pedidos.append(params)
        if "esearch" in url:
            if ids is None:  # NCBI contesta un error y no una lista de resultados
                return RespuestaFalsa(json={"esearchresult": {"ERROR": "Invalid db name specified"}})
            return RespuestaFalsa(json={"esearchresult": {"idlist": ids}})
        texto = ">NM_1\nACGT\n" if params["rettype"] == "fasta" else "FEATURES\n"
        return RespuestaFalsa(texto=texto)

    monkeypatch.setattr("requests.get", get)


def test_cp16_consultar_entrez_devuelve_la_secuencia_y_la_anotacion(monkeypatch):
    falso_ncbi(monkeypatch, ids=["123"])
    respuesta = consultar_entrez("NM_1", "Homo sapiens")
    assert respuesta["fasta"].startswith(">NM_1") and respuesta["genbank"].startswith("FEATURES")


def test_cp17_consultar_entrez_sin_resultados_lanza_target_no_encontrado(monkeypatch):
    falso_ncbi(monkeypatch, ids=[])
    with pytest.raises(TargetNoEncontrado):
        consultar_entrez("NM_X", "Homo sapiens")


def test_cp18_con_las_respuestas_grabadas_se_obtiene_la_referencia_de_nm_000518():
    r = controlador_con_grabaciones().obtener("c1", "NM_000518", "Homo sapiens")
    assert r.obtenida and len(r.referencia.secuencia) == 628


def test_cp20_un_identificador_con_sintaxis_de_busqueda_se_trata_como_no_encontrado():
    consultas = []
    adaptador = AdaptadorNcbiEntrez(lambda i, o: consultas.append((i, o)) or {})
    with pytest.raises(TargetNoEncontrado):
        adaptador.obtener_referencia("BRCA1 OR TP53", "Homo sapiens")
    assert consultas == []  # ni siquiera se consulta a NCBI


def test_cp21_un_organismo_con_sintaxis_de_busqueda_se_trata_como_no_encontrado():
    adaptador = AdaptadorNcbiEntrez(lambda i, o: {})
    with pytest.raises(TargetNoEncontrado):
        adaptador.obtener_referencia("NM_000518", "Homo sapiens[Organism] OR x")


def test_cp22_el_adaptador_ignora_los_espacios_sobrantes_del_identificador_y_el_organismo():
    recibido = []
    respuesta = {"fasta": ">x\nACGT\n", "genbank": ""}
    AdaptadorNcbiEntrez(lambda i, o: recibido.append((i, o)) or respuesta).obtener_referencia(" NM_000518 ", " Homo sapiens ")
    assert recibido == [("NM_000518", "Homo sapiens")]


def test_cp19_un_registro_sin_secuencia_se_rechaza_como_no_encontrado():
    r = controlador_con_grabaciones().obtener("c1", "NM_SIN_SECUENCIA", "Homo sapiens")
    assert not r.obtenida and r.aviso.codigo == "TARGET_NO_ENCONTRADO"


def test_cp23_una_respuesta_sin_fasta_ni_genbank_devuelve_datos_vacios():
    datos = AdaptadorNcbiEntrez(lambda i, o: {}).obtener_referencia("NM_1", "Homo sapiens")
    assert datos.secuencia == "" and datos.anotacion == ""


def test_cp24_las_respuestas_grabadas_no_valen_para_otro_organismo():
    with pytest.raises(TargetNoEncontrado):
        consultar_grabacion("NM_000518", "Mus musculus")


def test_cp25_consultar_entrez_busca_por_codigo_de_acceso_y_organismo_y_pide_el_primer_resultado(monkeypatch):
    pedidos = []
    falso_ncbi(monkeypatch, ids=["123", "456"], pedidos=pedidos)
    consultar_entrez("NM_1", "Mus musculus")
    busqueda, descargas = pedidos[0], pedidos[1:]
    assert busqueda["term"] == "NM_1[Accession] AND Mus musculus[Organism]"
    assert {pedido["id"] for pedido in descargas} == {"123"}


def test_cp28_consultar_entrez_no_confunde_un_error_de_ncbi_con_un_target_inexistente(monkeypatch):
    falso_ncbi(monkeypatch, ids=None)
    with pytest.raises(RuntimeError):  # una falla del servicio, no TargetNoEncontrado (DA-03)
        consultar_entrez("NM_1", "Homo sapiens")


def test_cp27_consultar_entrez_espera_entre_pedidos_para_respetar_el_limite_de_ncbi(monkeypatch):
    falso_ncbi(monkeypatch, ids=["123"])
    esperas = []
    monkeypatch.setattr("time.sleep", esperas.append)
    consultar_entrez("NM_1", "Homo sapiens")
    assert len(esperas) == 2 and all(espera >= 0.34 for espera in esperas)  # NCBI admite 3 pedidos por segundo


VARIANTES_DEL_FASTA = {
    "saltos de línea de Windows": ">x\r\nACGT\r\nAC\r\n",
    "línea en blanco al final": ">x\nACGT\nAC\n\n",
    "cabecera vacía": ">\nACGTAC\n",
}


@pytest.mark.parametrize("fasta", VARIANTES_DEL_FASTA.values(), ids=VARIANTES_DEL_FASTA.keys())
def test_cp26_el_adaptador_obtiene_la_secuencia_aunque_cambie_la_forma_del_fasta(fasta):  # EC-04
    respuesta = {"fasta": fasta, "genbank": "", "campo_nuevo": 1}
    datos = AdaptadorNcbiEntrez(lambda i, o: respuesta).obtener_referencia("NM_1", "Homo sapiens")
    assert datos.secuencia == "ACGTAC"
