import sys
from datetime import date
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sgsa.dominio.enums import Prioridad, TipoSolicitud  # noqa: E402
from sgsa.dominio.modelos import DatosNuevaSolicitud, Estudiante  # noqa: E402
from sgsa.persistencia.repositorio_memoria import RepositorioEnMemoria  # noqa: E402
from sgsa.servicios.servicio_solicitudes import ServicioSolicitudes  # noqa: E402

FECHA_BASE = date(2026, 10, 1)


@pytest.fixture
def repositorio():
    return RepositorioEnMemoria()


@pytest.fixture
def servicio(repositorio):
    return ServicioSolicitudes(repositorio)


@pytest.fixture
def estudiante(servicio):
    return servicio.registrar_estudiante(Estudiante("10234", "Ana", "Perez", "ana.perez@mail.com"))


@pytest.fixture
def nueva_solicitud(estudiante):
    def _crear(tipo=TipoSolicitud.CERTIFICADO, prioridad=Prioridad.BAJA, fecha=FECHA_BASE,
               descripcion="Descripcion de prueba valida"):
        return DatosNuevaSolicitud(estudiante, tipo, descripcion, prioridad, fecha)
    return _crear
