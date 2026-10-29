"""Interfaz de consola: solo pide datos, delega en los servicios y muestra resultados."""
import json
import sys
from typing import Callable, Dict, Optional, Tuple

from sgsa import config
from sgsa.dominio import reglas
from sgsa.dominio.enums import Estado, Prioridad, TipoSolicitud
from sgsa.dominio.excepciones import DatoInvalidoError, ErrorSGSA
from sgsa.dominio.modelos import DatosNuevaSolicitud, Estudiante
from sgsa.dominio.validadores import validar_descripcion, validar_email, validar_nombre_completo
from sgsa.persistencia.repositorio_json import RepositorioJSON
from sgsa.servicios.servicio_reportes import ServicioReportes
from sgsa.servicios.servicio_solicitudes import FiltroSolicitudes, ServicioSolicitudes
from sgsa.ui import formato

TITULO_MENU = "===== SGSA - Gestion de Solicitudes Academicas ====="
OPCION_SALIR = "0"


def leer(mensaje: str) -> str:
    return input(mensaje).strip()


def leer_entero(mensaje: str) -> int:
    try:
        return int(input(mensaje))
    except ValueError:
        raise DatoInvalidoError("numero invalido")


def leer_codigo(mensaje: str, conversor: Callable, error: str):
    try:
        return conversor(leer(mensaje).upper())
    except ValueError:
        raise DatoInvalidoError(error)


class ConsolaSGSA:

    def __init__(self, solicitudes: ServicioSolicitudes, reportes: ServicioReportes):
        self._solicitudes = solicitudes
        self._reportes = reportes
        self._opciones: Dict[str, Tuple[str, Callable[[], None]]] = {
            "1": ("Registrar estudiante", self.registrar_estudiante),
            "2": ("Registrar solicitud", self.registrar_solicitud),
            "3": ("Cambiar estado de solicitud", self.cambiar_estado),
            "4": ("Asignar responsable", self.asignar_responsable),
            "5": ("Buscar / filtrar solicitudes", self.buscar),
            "6": ("Reporte basico", self.reporte),
        }

    # ---------- bucle principal ----------
    def ejecutar(self) -> None:
        while True:
            self._mostrar_menu()
            opcion = leer("Opcion: ")
            if opcion == OPCION_SALIR:
                print("Hasta luego")
                return
            self._ejecutar_opcion(opcion)

    def _mostrar_menu(self) -> None:
        print("")
        print(TITULO_MENU)
        for clave, (descripcion, _) in self._opciones.items():
            print(f"{clave}. {descripcion}")
        print(f"{OPCION_SALIR}. Salir")

    def _ejecutar_opcion(self, opcion: str) -> None:
        if opcion not in self._opciones:
            print("Opcion invalida")
            return
        _, accion = self._opciones[opcion]
        try:
            accion()
        except ErrorSGSA as error:
            print(f"Error: {error}")

    # ---------- casos de uso ----------
    def registrar_estudiante(self) -> None:
        print("--- Registrar estudiante ---")
        legajo = leer("Legajo: ")
        self._solicitudes.verificar_legajo_disponible(legajo)
        nombre = leer("Nombre: ")
        apellido = leer("Apellido: ")
        validar_nombre_completo(nombre, apellido)
        email = validar_email(leer("Email: "))
        estudiante = self._solicitudes.registrar_estudiante(Estudiante(legajo, nombre, apellido, email))
        print(f"Estudiante registrado: {estudiante.nombre_para_mostrar}")

    def registrar_solicitud(self) -> None:
        print("--- Registrar solicitud ---")
        estudiante = self._solicitudes.obtener_estudiante(leer("Legajo del estudiante: "))
        print(formato.leyenda_tipos())
        tipo = leer_codigo("Tipo: ", TipoSolicitud.desde_codigo, "tipo invalido")
        descripcion = validar_descripcion(leer("Descripcion: "))
        prioridad = self._leer_prioridad(tipo)
        datos = DatosNuevaSolicitud(estudiante, tipo, descripcion, prioridad, config.fecha_hoy())
        solicitud = self._solicitudes.registrar_solicitud(datos)
        print(f"Solicitud #{solicitud.id} registrada para {estudiante.nombre_para_mostrar}")

    def _leer_prioridad(self, tipo: TipoSolicitud) -> Prioridad:
        respuesta = leer(formato.leyenda_prioridades())
        if respuesta == "":
            return reglas.prioridad_automatica(tipo)
        niveles_validos = {str(p.nivel): p for p in Prioridad}
        if respuesta not in niveles_validos:
            raise DatoInvalidoError("prioridad invalida")
        return niveles_validos[respuesta]

    def cambiar_estado(self) -> None:
        print("--- Cambiar estado ---")
        solicitud = self._solicitudes.obtener_solicitud(leer_entero("Nro de solicitud: "))
        print(formato.leyenda_estados())
        nuevo_estado = leer_codigo("Nuevo estado: ", Estado.desde_codigo, "estado invalido")
        self._solicitudes.cambiar_estado(solicitud.id, nuevo_estado)
        print(f"Solicitud #{solicitud.id} ahora esta {nuevo_estado.descripcion}")

    def asignar_responsable(self) -> None:
        print("--- Asignar responsable ---")
        solicitud = self._solicitudes.obtener_solicitud(leer_entero("Nro de solicitud: "))
        solicitud.verificar_que_este_abierta()
        for responsable in self._solicitudes.listar_responsables():
            print(f"{responsable.id}) {responsable.nombre} - {responsable.area}")
        responsable_id = leer_entero("Responsable: ")
        responsable = self._solicitudes.asignar_responsable(solicitud.id, responsable_id)
        print(f"Solicitud #{solicitud.id} asignada a {responsable.nombre}")

    def buscar(self) -> None:
        print("--- Buscar / filtrar ---")
        print("Filtrar por: 1) Estado 2) Tipo 3) Legajo 4) Todas")
        filtro = self._leer_filtro(leer("Opcion: "))
        encontradas = self._solicitudes.buscar(filtro)
        if not encontradas:
            print("No se encontraron solicitudes")
            return
        for solicitud in encontradas:
            print(formato.fila_solicitud(solicitud, self._solicitudes.nombre_responsable(solicitud)))

    def _leer_filtro(self, opcion: str) -> FiltroSolicitudes:
        if opcion == "1":
            return FiltroSolicitudes(estado=leer(f"Estado ({formato.codigos_estado()}): ").upper())
        if opcion == "2":
            return FiltroSolicitudes(tipo=leer(f"Tipo ({formato.codigos_tipo()}): ").upper())
        if opcion == "3":
            return FiltroSolicitudes(legajo=leer("Legajo: "))
        if opcion == "4":
            return FiltroSolicitudes()
        raise DatoInvalidoError("opcion invalida")

    def reporte(self) -> None:
        print("--- Reporte basico ---")
        for linea in formato.lineas_reporte(self._reportes.generar(config.fecha_hoy())):
            print(linea)


def construir_consola(ruta_datos: Optional[str] = None) -> ConsolaSGSA:
    """Composition root: unico lugar donde se eligen las implementaciones concretas."""
    repositorio = RepositorioJSON(ruta_datos or config.ruta_datos())
    return ConsolaSGSA(ServicioSolicitudes(repositorio), ServicioReportes(repositorio))


def main() -> None:
    try:
        consola = construir_consola()
    except (json.JSONDecodeError, KeyError, ValueError) as error:
        print(f"Error: el archivo de datos esta danado y no se puede abrir ({error})")
        sys.exit(1)
    consola.ejecutar()
