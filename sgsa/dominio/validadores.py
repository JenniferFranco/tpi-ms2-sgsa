"""Validaciones reutilizables (antes estaban copiadas en varios metodos)."""
from sgsa.dominio.excepciones import DatoInvalidoError

LONGITUD_MINIMA_LEGAJO = 4
LONGITUD_MAXIMA_LEGAJO = 6
LONGITUD_MINIMA_DESCRIPCION = 10


def validar_legajo(legajo: str) -> str:
    longitud_valida = LONGITUD_MINIMA_LEGAJO <= len(legajo) <= LONGITUD_MAXIMA_LEGAJO
    if not legajo.isdigit() or not longitud_valida:
        raise DatoInvalidoError("legajo invalido (4 a 6 digitos)")
    return legajo


def validar_nombre_completo(nombre: str, apellido: str) -> None:
    if not nombre or not apellido:
        raise DatoInvalidoError("nombre y apellido son obligatorios")


def validar_email(email: str) -> str:
    dominio = email.split("@")[-1]
    if "@" not in email or "." not in dominio:
        raise DatoInvalidoError("email invalido")
    return email


def validar_descripcion(descripcion: str) -> str:
    if len(descripcion) < LONGITUD_MINIMA_DESCRIPCION:
        raise DatoInvalidoError("la descripcion debe tener al menos 10 caracteres")
    return descripcion
