"""Entidades del dominio. La logica de estado vive en Solicitud (Move Method)."""
from dataclasses import dataclass
from datetime import date
from typing import Optional

from sgsa.dominio import reglas
from sgsa.dominio.enums import Estado, Prioridad, TipoSolicitud
from sgsa.dominio.excepciones import OperacionNoPermitidaError


@dataclass
class Estudiante:
    legajo: str
    nombre: str
    apellido: str
    email: str

    @property
    def nombre_para_mostrar(self) -> str:
        return f"{self.apellido}, {self.nombre}"


@dataclass(frozen=True)
class Responsable:
    id: int
    nombre: str
    area: str


@dataclass(frozen=True)
class DatosNuevaSolicitud:
    """Parameter Object: reemplaza los 9 parametros sueltos de crear_solicitud()."""
    estudiante: Estudiante
    tipo: TipoSolicitud
    descripcion: str
    prioridad: Prioridad
    fecha: date


@dataclass
class Solicitud:
    id: int
    legajo: str
    tipo: TipoSolicitud
    descripcion: str
    prioridad: Prioridad
    fecha: date
    estado: Estado = Estado.PENDIENTE
    responsable_id: Optional[int] = None

    @classmethod
    def desde_datos(cls, id_solicitud: int, datos: DatosNuevaSolicitud) -> "Solicitud":
        return cls(id=id_solicitud, legajo=datos.estudiante.legajo, tipo=datos.tipo,
                   descripcion=datos.descripcion, prioridad=datos.prioridad, fecha=datos.fecha)

    @property
    def tiene_responsable(self) -> bool:
        return self.responsable_id is not None

    def cambiar_estado(self, nuevo_estado: Estado) -> None:
        if not reglas.transicion_permitida(self.estado, nuevo_estado):
            raise OperacionNoPermitidaError("transicion no permitida")
        if nuevo_estado is Estado.EN_PROCESO and not self.tiene_responsable:
            raise OperacionNoPermitidaError("debe asignar un responsable antes")
        self.estado = nuevo_estado

    def verificar_que_este_abierta(self) -> None:
        if self.estado.esta_cerrada:
            raise OperacionNoPermitidaError("la solicitud ya esta cerrada")

    def asignar_responsable(self, responsable: Responsable) -> None:
        self.verificar_que_este_abierta()
        self.responsable_id = responsable.id
        if self.estado is Estado.PENDIENTE:
            self.estado = Estado.EN_PROCESO

    def esta_vencida(self, hoy: date) -> bool:
        return self.estado is Estado.PENDIENTE and (hoy - self.fecha) > reglas.PLAZO_MAXIMO_SIN_ATENDER

    def es_prioritaria_abierta(self) -> bool:
        return self.prioridad is Prioridad.ALTA and self.estado.esta_abierta
