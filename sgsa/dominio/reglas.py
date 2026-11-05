"""Reglas de negocio configurables (OCP: se extienden agregando datos, no ifs)."""
from datetime import timedelta

from sgsa.dominio.enums import Estado, Prioridad, TipoSolicitud

PRIORIDAD_AUTOMATICA_POR_TIPO = {
    TipoSolicitud.RECLAMO_NOTA: Prioridad.ALTA,
    TipoSolicitud.MESA_ESPECIAL: Prioridad.ALTA,
    TipoSolicitud.EQUIVALENCIA: Prioridad.MEDIA,
    TipoSolicitud.CERTIFICADO: Prioridad.BAJA,
}

TRANSICIONES_PERMITIDAS = {
    Estado.PENDIENTE: {Estado.EN_PROCESO, Estado.RECHAZADA},
    Estado.EN_PROCESO: {Estado.RESUELTA, Estado.RECHAZADA},
    Estado.RESUELTA: set(),
    Estado.RECHAZADA: set(),
}

DIAS_MAXIMOS_SIN_ATENDER = 3
PLAZO_MAXIMO_SIN_ATENDER = timedelta(days=DIAS_MAXIMOS_SIN_ATENDER)


def prioridad_automatica(tipo: TipoSolicitud) -> Prioridad:
    return PRIORIDAD_AUTOMATICA_POR_TIPO[tipo]


def transicion_permitida(actual: Estado, nuevo: Estado) -> bool:
    return nuevo in TRANSICIONES_PERMITIDAS[actual]
