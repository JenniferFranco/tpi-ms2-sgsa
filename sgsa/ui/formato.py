"""Textos y formatos de presentacion (separados de la logica de negocio)."""
from typing import Optional

from sgsa.dominio import reglas
from sgsa.dominio.enums import Estado, Prioridad, TipoSolicitud
from sgsa.dominio.modelos import Solicitud
from sgsa.servicios.servicio_reportes import ReporteBasico

SIN_RESPONSABLE = "-"


def leyenda_tipos() -> str:
    return "Tipos: " + ", ".join(f"{t.codigo}={t.descripcion}" for t in TipoSolicitud)


def leyenda_estados() -> str:
    return "Estados: " + ", ".join(f"{e.codigo}={e.descripcion}" for e in Estado)


def leyenda_prioridades() -> str:
    niveles = ", ".join(f"{p.nivel}={p.descripcion}" for p in Prioridad)
    return f"Prioridad ({niveles}, Enter=automatica): "


def codigos_estado() -> str:
    return "/".join(e.codigo for e in Estado)


def codigos_tipo() -> str:
    return "/".join(t.codigo for t in TipoSolicitud)


def fila_solicitud(solicitud: Solicitud, nombre_responsable: Optional[str]) -> str:
    return (f"#{solicitud.id} | {solicitud.tipo.codigo} | {solicitud.estado.descripcion} | "
            f"Prioridad: {solicitud.prioridad.descripcion} | Legajo: {solicitud.legajo} | "
            f"Resp: {nombre_responsable or SIN_RESPONSABLE}")


def lineas_reporte(reporte: ReporteBasico) -> list:
    por_estado = " | ".join(f"{e.descripcion}: {n}" for e, n in reporte.por_estado.items())
    por_tipo = " | ".join(f"{t.codigo}: {n}" for t, n in reporte.por_tipo.items())
    lineas = [
        f"Total de solicitudes: {reporte.total}",
        f"Por estado -> {por_estado}",
        f"Por tipo -> {por_tipo}",
        f"Abiertas con prioridad alta: {reporte.abiertas_prioridad_alta}",
        f"Pendientes con mas de {reglas.DIAS_MAXIMOS_SIN_ATENDER} dias sin atender: "
        f"{len(reporte.pendientes_vencidas)}",
    ]
    lineas += [f"  #{s.id} ({s.tipo.codigo}) desde {s.fecha.isoformat()}"
               for s in reporte.pendientes_vencidas]
    return lineas
