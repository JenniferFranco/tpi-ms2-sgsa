"""Casos de uso del sistema. No hace input()/print(): eso es tarea de la UI (SRP)."""
from dataclasses import dataclass
from typing import Callable, List, Optional

from sgsa.dominio.enums import Estado
from sgsa.dominio.excepciones import (EntidadDuplicadaError, EntidadNoEncontradaError)
from sgsa.dominio.modelos import DatosNuevaSolicitud, Estudiante, Responsable, Solicitud
from sgsa.dominio.validadores import (validar_descripcion, validar_email, validar_legajo,
                                      validar_nombre_completo)
from sgsa.persistencia.repositorio import RepositorioSGSA


@dataclass(frozen=True)
class FiltroSolicitudes:
    """Parameter Object para la busqueda: un solo criterio opcional por campo."""
    estado: Optional[str] = None
    tipo: Optional[str] = None
    legajo: Optional[str] = None

    def admite(self, solicitud: Solicitud) -> bool:
        return all(condicion(solicitud) for condicion in self._condiciones())

    def _condiciones(self) -> List[Callable[[Solicitud], bool]]:
        condiciones = []
        if self.estado is not None:
            condiciones.append(lambda s: s.estado.codigo == self.estado)
        if self.tipo is not None:
            condiciones.append(lambda s: s.tipo.codigo == self.tipo)
        if self.legajo is not None:
            condiciones.append(lambda s: s.legajo == self.legajo)
        return condiciones


class ServicioSolicitudes:

    def __init__(self, repositorio: RepositorioSGSA):
        self._repositorio = repositorio

    # ---------- estudiantes ----------
    def verificar_legajo_disponible(self, legajo: str) -> None:
        validar_legajo(legajo)
        if self._repositorio.buscar_estudiante(legajo):
            raise EntidadDuplicadaError("ya existe un estudiante con ese legajo")

    def registrar_estudiante(self, estudiante: Estudiante) -> Estudiante:
        self.verificar_legajo_disponible(estudiante.legajo)
        validar_nombre_completo(estudiante.nombre, estudiante.apellido)
        validar_email(estudiante.email)
        self._repositorio.agregar_estudiante(estudiante)
        return estudiante

    def obtener_estudiante(self, legajo: str) -> Estudiante:
        validar_legajo(legajo)
        estudiante = self._repositorio.buscar_estudiante(legajo)
        if estudiante is None:
            raise EntidadNoEncontradaError("el estudiante no existe")
        return estudiante

    # ---------- solicitudes ----------
    def registrar_solicitud(self, datos: DatosNuevaSolicitud) -> Solicitud:
        validar_descripcion(datos.descripcion)
        return self._repositorio.crear_solicitud(datos)

    def obtener_solicitud(self, solicitud_id: int) -> Solicitud:
        solicitud = self._repositorio.buscar_solicitud(solicitud_id)
        if solicitud is None:
            raise EntidadNoEncontradaError("la solicitud no existe")
        return solicitud

    def cambiar_estado(self, solicitud_id: int, nuevo_estado: Estado) -> Solicitud:
        solicitud = self.obtener_solicitud(solicitud_id)
        solicitud.cambiar_estado(nuevo_estado)
        self._repositorio.actualizar_solicitud(solicitud)
        return solicitud

    def listar_responsables(self) -> List[Responsable]:
        return self._repositorio.listar_responsables()

    def obtener_responsable(self, responsable_id: int) -> Responsable:
        responsable = self._repositorio.buscar_responsable(responsable_id)
        if responsable is None:
            raise EntidadNoEncontradaError("el responsable no existe")
        return responsable

    def asignar_responsable(self, solicitud_id: int, responsable_id: int) -> Responsable:
        solicitud = self.obtener_solicitud(solicitud_id)
        responsable = self.obtener_responsable(responsable_id)
        solicitud.asignar_responsable(responsable)
        self._repositorio.actualizar_solicitud(solicitud)
        return responsable

    def buscar(self, filtro: FiltroSolicitudes) -> List[Solicitud]:
        if filtro.legajo is not None:
            validar_legajo(filtro.legajo)
        encontradas = [s for s in self._repositorio.listar_solicitudes() if filtro.admite(s)]
        return sorted(encontradas, key=lambda s: (s.prioridad.nivel, s.id))

    def nombre_responsable(self, solicitud: Solicitud) -> Optional[str]:
        responsable = self._repositorio.buscar_responsable(solicitud.responsable_id)
        return responsable.nombre if responsable else None
