"""Tipos enumerados del dominio (reemplazan los codigos magicos de la version inicial)."""
from enum import Enum


class Estado(Enum):
    PENDIENTE = ("P", "Pendiente")
    EN_PROCESO = ("EP", "En proceso")
    RESUELTA = ("R", "Resuelta")
    RECHAZADA = ("X", "Rechazada")

    def __init__(self, codigo: str, descripcion: str):
        self.codigo = codigo
        self.descripcion = descripcion

    @classmethod
    def desde_codigo(cls, codigo: str) -> "Estado":
        for estado in cls:
            if estado.codigo == codigo:
                return estado
        raise ValueError(f"Estado desconocido: {codigo}")

    @property
    def esta_cerrada(self) -> bool:
        return self in (Estado.RESUELTA, Estado.RECHAZADA)

    @property
    def esta_abierta(self) -> bool:
        return not self.esta_cerrada


class Prioridad(Enum):
    ALTA = (1, "Alta")
    MEDIA = (2, "Media")
    BAJA = (3, "Baja")

    def __init__(self, nivel: int, descripcion: str):
        self.nivel = nivel
        self.descripcion = descripcion

    @classmethod
    def desde_nivel(cls, nivel: int) -> "Prioridad":
        for prioridad in cls:
            if prioridad.nivel == nivel:
                return prioridad
        raise ValueError(f"Prioridad desconocida: {nivel}")


class TipoSolicitud(Enum):
    CERTIFICADO = ("CERT", "Certificado")
    EQUIVALENCIA = ("EQUIV", "Equivalencia")
    MESA_ESPECIAL = ("MESA", "Mesa especial")
    RECLAMO_NOTA = ("RECL", "Reclamo de nota")

    def __init__(self, codigo: str, descripcion: str):
        self.codigo = codigo
        self.descripcion = descripcion

    @classmethod
    def desde_codigo(cls, codigo: str) -> "TipoSolicitud":
        for tipo in cls:
            if tipo.codigo == codigo:
                return tipo
        raise ValueError(f"Tipo desconocido: {codigo}")
