"""Configuracion del sistema: ruta del archivo de datos y fecha de referencia."""
import os
from datetime import date, datetime

RUTA_DATOS_POR_DEFECTO = "datos.json"
FORMATO_FECHA = "%Y-%m-%d"


def ruta_datos() -> str:
    return os.environ.get("SGSA_DATA", RUTA_DATOS_POR_DEFECTO)


def fecha_hoy() -> date:
    """Devuelve la fecha actual; SGSA_HOY permite simularla en pruebas."""
    fecha_simulada = os.environ.get("SGSA_HOY")
    if fecha_simulada:
        return datetime.strptime(fecha_simulada, FORMATO_FECHA).date()
    return date.today()
