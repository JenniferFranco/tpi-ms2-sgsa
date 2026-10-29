"""Abstraccion de persistencia (DIP): los servicios dependen de esta interfaz."""
from abc import ABC, abstractmethod
from typing import List, Optional

from sgsa.dominio.modelos import DatosNuevaSolicitud, Estudiante, Responsable, Solicitud


class RepositorioSGSA(ABC):

    # --- estudiantes ---
    @abstractmethod
    def buscar_estudiante(self, legajo: str) -> Optional[Estudiante]: ...

    @abstractmethod
    def agregar_estudiante(self, estudiante: Estudiante) -> None: ...

    # --- responsables ---
    @abstractmethod
    def listar_responsables(self) -> List[Responsable]: ...

    def buscar_responsable(self, responsable_id: Optional[int]) -> Optional[Responsable]:
        return next((r for r in self.listar_responsables() if r.id == responsable_id), None)

    # --- solicitudes ---
    @abstractmethod
    def listar_solicitudes(self) -> List[Solicitud]: ...

    def buscar_solicitud(self, solicitud_id: int) -> Optional[Solicitud]:
        return next((s for s in self.listar_solicitudes() if s.id == solicitud_id), None)

    @abstractmethod
    def crear_solicitud(self, datos: DatosNuevaSolicitud) -> Solicitud: ...

    @abstractmethod
    def actualizar_solicitud(self, solicitud: Solicitud) -> None: ...
