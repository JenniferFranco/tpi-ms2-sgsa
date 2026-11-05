"""Repositorio en memoria: permite probar servicios sin tocar archivos."""
from typing import Dict, List, Optional

from sgsa.dominio.modelos import DatosNuevaSolicitud, Estudiante, Responsable, Solicitud
from sgsa.persistencia.repositorio import RepositorioSGSA

RESPONSABLES_INICIALES = [
    Responsable(1, "Laura Gomez", "Alumnado"),
    Responsable(2, "Martin Ruiz", "Secretaria Academica"),
    Responsable(3, "Sofia Diaz", "Bedelia"),
]


class RepositorioEnMemoria(RepositorioSGSA):
    """Implementacion base; RepositorioJSON la extiende agregando persistencia."""

    def __init__(self, responsables: Optional[List[Responsable]] = None):
        self._estudiantes: Dict[str, Estudiante] = {}
        self._responsables: List[Responsable] = list(responsables or RESPONSABLES_INICIALES)
        self._solicitudes: List[Solicitud] = []
        self._ultimo_id = 0

    def buscar_estudiante(self, legajo: str) -> Optional[Estudiante]:
        return self._estudiantes.get(legajo)

    def agregar_estudiante(self, estudiante: Estudiante) -> None:
        self._estudiantes[estudiante.legajo] = estudiante
        self._guardar()

    def listar_responsables(self) -> List[Responsable]:
        return list(self._responsables)

    def listar_solicitudes(self) -> List[Solicitud]:
        return list(self._solicitudes)

    def crear_solicitud(self, datos: DatosNuevaSolicitud) -> Solicitud:
        self._ultimo_id += 1
        solicitud = Solicitud.desde_datos(self._ultimo_id, datos)
        self._solicitudes.append(solicitud)
        self._guardar()
        return solicitud

    def actualizar_solicitud(self, solicitud: Solicitud) -> None:
        self._guardar()

    def _guardar(self) -> None:
        """En memoria no hay nada que persistir (hook para subclases)."""
