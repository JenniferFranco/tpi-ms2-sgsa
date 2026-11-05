"""Persistencia en archivo JSON, compatible con el formato de la version inicial."""
import json
from datetime import datetime
from pathlib import Path

from sgsa.config import FORMATO_FECHA
from sgsa.dominio.enums import Estado, Prioridad, TipoSolicitud
from sgsa.dominio.modelos import Estudiante, Responsable, Solicitud
from sgsa.persistencia.repositorio_memoria import RepositorioEnMemoria


class RepositorioJSON(RepositorioEnMemoria):

    def __init__(self, ruta: str):
        super().__init__()
        self._ruta = Path(ruta)
        if self._ruta.exists():
            self._cargar()

    # ---------- lectura ----------
    def _cargar(self) -> None:
        # Si el archivo existe pero esta corrupto, el error se propaga:
        # la version inicial lo ocultaba con "except: pass" y perdia los datos.
        contenido = json.loads(self._ruta.read_text(encoding="utf-8"))
        self._estudiantes = {e["legajo"]: Estudiante(**e) for e in contenido["estudiantes"]}
        self._responsables = [Responsable(**r) for r in contenido["responsables"]]
        self._solicitudes = [self._solicitud_desde_dict(s) for s in contenido["solicitudes"]]
        self._ultimo_id = contenido["ultimo_id"]

    @staticmethod
    def _solicitud_desde_dict(registro: dict) -> Solicitud:
        return Solicitud(
            id=registro["id"],
            legajo=registro["legajo"],
            tipo=TipoSolicitud.desde_codigo(registro["tipo"]),
            descripcion=registro["descripcion"],
            prioridad=Prioridad.desde_nivel(registro["prioridad"]),
            fecha=datetime.strptime(registro["fecha"], FORMATO_FECHA).date(),
            estado=Estado.desde_codigo(registro["estado"]),
            responsable_id=registro["responsable"],
        )

    # ---------- escritura ----------
    def _guardar(self) -> None:
        contenido = {
            "estudiantes": [vars(e) for e in self._estudiantes.values()],
            "responsables": [vars(r) for r in self._responsables],
            "solicitudes": [self._solicitud_a_dict(s) for s in self._solicitudes],
            "ultimo_id": self._ultimo_id,
        }
        self._ruta.write_text(json.dumps(contenido, indent=2, ensure_ascii=False), encoding="utf-8")

    @staticmethod
    def _solicitud_a_dict(solicitud: Solicitud) -> dict:
        return {
            "id": solicitud.id,
            "legajo": solicitud.legajo,
            "tipo": solicitud.tipo.codigo,
            "descripcion": solicitud.descripcion,
            "prioridad": solicitud.prioridad.nivel,
            "estado": solicitud.estado.codigo,
            "responsable": solicitud.responsable_id,
            "fecha": solicitud.fecha.strftime(FORMATO_FECHA),
        }
