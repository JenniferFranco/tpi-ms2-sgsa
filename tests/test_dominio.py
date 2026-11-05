"""Pruebas unitarias del dominio: enums, reglas y comportamiento de Solicitud."""
from datetime import date

import pytest

from sgsa.dominio import reglas
from sgsa.dominio.enums import Estado, Prioridad, TipoSolicitud
from sgsa.dominio.excepciones import OperacionNoPermitidaError
from sgsa.dominio.modelos import Responsable, Solicitud

RESPONSABLE = Responsable(2, "Martin Ruiz", "Secretaria Academica")


def solicitud(estado=Estado.PENDIENTE, responsable_id=None, prioridad=Prioridad.BAJA,
              fecha=date(2026, 10, 1)):
    return Solicitud(1, "10234", TipoSolicitud.CERTIFICADO, "Descripcion valida", prioridad,
                     fecha, estado, responsable_id)


@pytest.mark.parametrize("codigo,estado", [("P", Estado.PENDIENTE), ("EP", Estado.EN_PROCESO),
                                           ("R", Estado.RESUELTA), ("X", Estado.RECHAZADA)])
def test_estado_desde_codigo(codigo, estado):
    assert Estado.desde_codigo(codigo) is estado


def test_codigo_desconocido_lanza_error():
    with pytest.raises(ValueError):
        TipoSolicitud.desde_codigo("TRAMITE")


@pytest.mark.parametrize("tipo,esperada", [
    (TipoSolicitud.RECLAMO_NOTA, Prioridad.ALTA), (TipoSolicitud.MESA_ESPECIAL, Prioridad.ALTA),
    (TipoSolicitud.EQUIVALENCIA, Prioridad.MEDIA), (TipoSolicitud.CERTIFICADO, Prioridad.BAJA)])
def test_prioridad_automatica_por_tipo(tipo, esperada):
    assert reglas.prioridad_automatica(tipo) is esperada


def test_todo_tipo_tiene_prioridad_automatica():
    # Protege OCP: si se agrega un tipo nuevo sin regla, esta prueba avisa.
    assert set(reglas.PRIORIDAD_AUTOMATICA_POR_TIPO) == set(TipoSolicitud)


@pytest.mark.parametrize("actual,nuevo", [
    (Estado.PENDIENTE, Estado.RECHAZADA), (Estado.EN_PROCESO, Estado.RESUELTA),
    (Estado.EN_PROCESO, Estado.RECHAZADA)])
def test_transiciones_permitidas(actual, nuevo):
    s = solicitud(estado=actual, responsable_id=2)
    s.cambiar_estado(nuevo)
    assert s.estado is nuevo


@pytest.mark.parametrize("actual,nuevo", [
    (Estado.PENDIENTE, Estado.RESUELTA), (Estado.EN_PROCESO, Estado.PENDIENTE),
    (Estado.RESUELTA, Estado.EN_PROCESO), (Estado.RECHAZADA, Estado.PENDIENTE)])
def test_transiciones_no_permitidas(actual, nuevo):
    s = solicitud(estado=actual, responsable_id=2)
    with pytest.raises(OperacionNoPermitidaError, match="transicion no permitida"):
        s.cambiar_estado(nuevo)


def test_pasar_a_en_proceso_requiere_responsable():
    with pytest.raises(OperacionNoPermitidaError, match="responsable"):
        solicitud().cambiar_estado(Estado.EN_PROCESO)


def test_asignar_responsable_a_pendiente_la_pasa_a_en_proceso():
    s = solicitud()
    s.asignar_responsable(RESPONSABLE)
    assert s.responsable_id == 2 and s.estado is Estado.EN_PROCESO


@pytest.mark.parametrize("estado", [Estado.RESUELTA, Estado.RECHAZADA])
def test_no_se_asigna_responsable_a_solicitud_cerrada(estado):
    with pytest.raises(OperacionNoPermitidaError, match="cerrada"):
        solicitud(estado=estado).asignar_responsable(RESPONSABLE)


@pytest.mark.parametrize("hoy,vencida", [(date(2026, 10, 4), False), (date(2026, 10, 5), True)])
def test_vencimiento_es_mayor_a_tres_dias(hoy, vencida):
    # valor limite: 3 dias exactos NO esta vencida, 4 dias SI
    assert solicitud().esta_vencida(hoy) is vencida


def test_solicitud_en_proceso_nunca_esta_vencida():
    assert not solicitud(estado=Estado.EN_PROCESO).esta_vencida(date(2026, 12, 31))


def test_prioritaria_abierta():
    assert solicitud(prioridad=Prioridad.ALTA).es_prioritaria_abierta()
    assert not solicitud(prioridad=Prioridad.ALTA, estado=Estado.RESUELTA).es_prioritaria_abierta()
