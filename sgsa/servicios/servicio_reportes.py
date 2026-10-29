"""Generacion del reporte basico (Extract Class desde GestorSolicitudes.reporte)."""
from collections import Counter
from dataclasses import dataclass
from datetime import date
from typing import Dict, List

from sgsa.dominio.enums import Estado, TipoSolicitud
from sgsa.dominio.modelos import Solicitud
from sgsa.persistencia.repositorio import RepositorioSGSA


@dataclass(frozen=True)
class ReporteBasico:
    total: int
    por_estado: Dict[Estado, int]
    por_tipo: Dict[TipoSolicitud, int]
    abiertas_prioridad_alta: int
    pendientes_vencidas: List[Solicitud]


class ServicioReportes:

    def __init__(self, repositorio: RepositorioSGSA):
        self._repositorio = repositorio

    def generar(self, hoy: date) -> ReporteBasico:
        solicitudes = self._repositorio.listar_solicitudes()
        return ReporteBasico(
            total=len(solicitudes),
            por_estado=self._contar(solicitudes, Estado, lambda s: s.estado),
            por_tipo=self._contar(solicitudes, TipoSolicitud, lambda s: s.tipo),
            abiertas_prioridad_alta=sum(1 for s in solicitudes if s.es_prioritaria_abierta()),
            pendientes_vencidas=[s for s in solicitudes if s.esta_vencida(hoy)],
        )

    @staticmethod
    def _contar(solicitudes, enumeracion, clave) -> Dict:
        conteo = Counter(clave(s) for s in solicitudes)
        return {valor: conteo.get(valor, 0) for valor in enumeracion}
