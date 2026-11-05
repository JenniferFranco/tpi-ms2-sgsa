"""Pruebas de los casos de uso con repositorio en memoria (posible gracias a DIP)."""
from datetime import date

import pytest

from sgsa.dominio.enums import Estado, Prioridad, TipoSolicitud
from sgsa.dominio.excepciones import (DatoInvalidoError, EntidadDuplicadaError,
                                      EntidadNoEncontradaError, OperacionNoPermitidaError)
from sgsa.dominio.modelos import Estudiante
from sgsa.servicios.servicio_reportes import ServicioReportes
from sgsa.servicios.servicio_solicitudes import FiltroSolicitudes


def test_no_se_registra_legajo_duplicado(servicio, estudiante):
    with pytest.raises(EntidadDuplicadaError):
        servicio.registrar_estudiante(Estudiante("10234", "Otra", "Persona", "otra@mail.com"))


def test_estudiante_inexistente(servicio):
    with pytest.raises(EntidadNoEncontradaError):
        servicio.obtener_estudiante("99999")


def test_registrar_solicitud_asigna_ids_correlativos(servicio, nueva_solicitud):
    primera = servicio.registrar_solicitud(nueva_solicitud())
    segunda = servicio.registrar_solicitud(nueva_solicitud())
    assert (primera.id, segunda.id) == (1, 2)
    assert primera.estado is Estado.PENDIENTE and primera.responsable_id is None


def test_registrar_solicitud_valida_descripcion(servicio, nueva_solicitud):
    with pytest.raises(DatoInvalidoError):
        servicio.registrar_solicitud(nueva_solicitud(descripcion="corta"))


def test_flujo_completo_asignar_y_resolver(servicio, nueva_solicitud):
    s = servicio.registrar_solicitud(nueva_solicitud())
    responsable = servicio.asignar_responsable(s.id, 3)
    assert responsable.nombre == "Sofia Diaz"
    assert servicio.cambiar_estado(s.id, Estado.RESUELTA).estado is Estado.RESUELTA


def test_asignar_responsable_inexistente(servicio, nueva_solicitud):
    s = servicio.registrar_solicitud(nueva_solicitud())
    with pytest.raises(EntidadNoEncontradaError, match="responsable"):
        servicio.asignar_responsable(s.id, 9)
    assert servicio.obtener_solicitud(s.id).estado is Estado.PENDIENTE


def test_cambiar_estado_de_solicitud_inexistente(servicio):
    with pytest.raises(EntidadNoEncontradaError):
        servicio.cambiar_estado(99, Estado.RECHAZADA)


def test_no_se_reabre_solicitud_rechazada(servicio, nueva_solicitud):
    s = servicio.registrar_solicitud(nueva_solicitud())
    servicio.cambiar_estado(s.id, Estado.RECHAZADA)
    with pytest.raises(OperacionNoPermitidaError):
        servicio.asignar_responsable(s.id, 1)


def test_busqueda_filtra_y_ordena_por_prioridad_e_id(servicio, nueva_solicitud):
    servicio.registrar_solicitud(nueva_solicitud(prioridad=Prioridad.BAJA))
    servicio.registrar_solicitud(nueva_solicitud(TipoSolicitud.RECLAMO_NOTA, Prioridad.ALTA))
    servicio.registrar_solicitud(nueva_solicitud(prioridad=Prioridad.BAJA))
    assert [s.id for s in servicio.buscar(FiltroSolicitudes())] == [2, 1, 3]
    assert [s.id for s in servicio.buscar(FiltroSolicitudes(tipo="CERT"))] == [1, 3]
    assert servicio.buscar(FiltroSolicitudes(estado="R")) == []


def test_busqueda_por_legajo_invalido(servicio):
    with pytest.raises(DatoInvalidoError):
        servicio.buscar(FiltroSolicitudes(legajo="12"))


def test_reporte_cuenta_por_estado_tipo_y_vencidas(repositorio, servicio, nueva_solicitud):
    servicio.registrar_solicitud(nueva_solicitud(TipoSolicitud.MESA_ESPECIAL, Prioridad.ALTA))
    servicio.registrar_solicitud(nueva_solicitud(fecha=date(2026, 10, 10)))
    tercera = servicio.registrar_solicitud(nueva_solicitud(TipoSolicitud.EQUIVALENCIA, Prioridad.MEDIA))
    servicio.asignar_responsable(tercera.id, 1)

    reporte = ServicioReportes(repositorio).generar(hoy=date(2026, 10, 12))

    assert reporte.total == 3
    assert reporte.por_estado[Estado.PENDIENTE] == 2 and reporte.por_estado[Estado.EN_PROCESO] == 1
    assert reporte.por_tipo[TipoSolicitud.RECLAMO_NOTA] == 0
    assert reporte.abiertas_prioridad_alta == 1
    assert [s.id for s in reporte.pendientes_vencidas] == [1]
