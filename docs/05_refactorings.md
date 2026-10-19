# Etapa 5 — Refactoring seguro

**Estrategia:** antes de cambiar una línea se fijó el comportamiento con pruebas golden master (tag `etapa-diagnostico`). Luego se construyó la nueva estructura **en paralelo** (módulos nuevos sin uso) y recién en el último commit se cambió `sistema.py` para usarla. Así cada commit intermedio mantiene el sistema funcionando y las pruebas en verde (técnica "strangler" / rama por abstracción).

| ID | Refactoring (catálogo de Fowler) | Antes (estado-inicial) | Después (estado-refactorizado) | Smell que resuelve |
|---|---|---|---|---|
| R1 | **Extract Method** | `registrar_solicitud()` (40 líneas, CC 19) validaba, calculaba prioridad y persistía. `buscar()` (CC 23) leía filtro, filtraba, traducía códigos e imprimía. | `_leer_prioridad()`, `_leer_filtro()`, `formato.fila_solicitud()`, `formato.lineas_reporte()`, `validar_*()`. Cada método ≤ CC 5. | CS-02, CS-03 |
| R2 | **Move Method** (reubicación de responsabilidad) | Reglas de transición, asignación y vencimiento escritas en la UI (`cambiar_estado`, `asignar_responsable`, `reporte`). | `Solicitud.cambiar_estado()`, `Solicitud.asignar_responsable()`, `Solicitud.esta_vencida()`, `Solicitud.es_prioritaria_abierta()`. | CS-01, CS-06 |
| R3 | **Introduce Parameter Object** | `crear_solicitud(legajo, nombre, apellido, email, tipo, descripcion, prioridad, responsable, fecha)` — 9 parámetros, 2 sin uso. | `DatosNuevaSolicitud(estudiante, tipo, descripcion, prioridad, fecha)`; además `FiltroSolicitudes(estado, tipo, legajo)` para la búsqueda. | CS-04 |
| R4 | **Replace Type Code with Class** + **Replace Magic Number with Symbolic Constant** | `"P"/"EP"/"R"/"X"`, `1/2/3`, `"CERT"…`, `3` días. | Enums `Estado`, `Prioridad`, `TipoSolicitud` (código + descripción) y constantes con nombre. | CS-05 |
| R5 | **Replace Conditional with Lookup Table** | if/elif de prioridad automática, `flag` de transiciones, contadores `c1..c4`. | `PRIORIDAD_AUTOMATICA_POR_TIPO`, `TRANSICIONES_PERMITIDAS`, `Counter` sobre los enums. | CS-06 |
| R6 | **Extract Class** + **Extract Interface** | Todo en `GestorSolicitudes` + global `datos`. | `ServicioSolicitudes`, `ServicioReportes`, `ConsolaSGSA`, `RepositorioSGSA` → `RepositorioEnMemoria` → `RepositorioJSON`. | CS-01, CS-08, CS-10 |
| R7 | **Replace Error Code with Exception** | `print("Error: …"); return` en cada método y `except:` desnudos. | `DatoInvalidoError`, `EntidadNoEncontradaError`, `EntidadDuplicadaError`, `OperacionNoPermitidaError`; captura única en la UI. | CS-07 |
| R8 | **Rename Variable / Method** | `d`, `t`, `flag`, `id`, `c1`… | Nombres del dominio. | CS-09 |

## Ejemplo antes/después — R3 (Introduce Parameter Object)
```python
# ANTES (sistema.py, L98-100)
self.crear_solicitud(est["legajo"], est["nombre"], est["apellido"], est["email"],
                     t, d, p, None, hoy().isoformat())
def crear_solicitud(self, legajo, nombre, apellido, email, tipo, descripcion,
                    prioridad, responsable, fecha): ...

# DESPUÉS (sgsa/dominio/modelos.py + ui/consola.py)
@dataclass(frozen=True)
class DatosNuevaSolicitud:
    estudiante: Estudiante
    tipo: TipoSolicitud
    descripcion: str
    prioridad: Prioridad
    fecha: date

datos = DatosNuevaSolicitud(estudiante, tipo, descripcion, prioridad, config.fecha_hoy())
solicitud = self._solicitudes.registrar_solicitud(datos)
```

## Ejemplo antes/después — R2 + R5 (Move Method + Lookup Table)
```python
# ANTES (sistema.py, L130-142, dentro de la UI)
flag = False
if s["estado"] == "P":
    if nuevo == "EP" or nuevo == "X":
        flag = True
elif s["estado"] == "EP":
    if nuevo == "R" or nuevo == "X":
        flag = True
if flag == False:
    print("Error: transicion no permitida"); return
if nuevo == "EP" and s["responsable"] == None:
    print("Error: debe asignar un responsable antes"); return

# DESPUÉS (sgsa/dominio/reglas.py + modelos.py)
TRANSICIONES_PERMITIDAS = {
    Estado.PENDIENTE: {Estado.EN_PROCESO, Estado.RECHAZADA},
    Estado.EN_PROCESO: {Estado.RESUELTA, Estado.RECHAZADA},
    Estado.RESUELTA: set(), Estado.RECHAZADA: set(),
}
def cambiar_estado(self, nuevo_estado: Estado) -> None:
    if not reglas.transicion_permitida(self.estado, nuevo_estado):
        raise OperacionNoPermitidaError("transicion no permitida")
    if nuevo_estado is Estado.EN_PROCESO and not self.tiene_responsable:
        raise OperacionNoPermitidaError("debe asignar un responsable antes")
    self.estado = nuevo_estado
```

## Garantía de seguridad
- Las 3 pruebas golden master dan **idéntica salida de consola e idéntico archivo JSON** en `estado-inicial` y `estado-refactorizado`.
- Formato del archivo de datos sin cambios: un `datos.json` creado con la versión inicial se abre con la refactorizada (prueba `test_lee_archivos_generados_por_la_version_inicial`).
- Único cambio de comportamiento, **intencional y documentado**: con un archivo de datos dañado, la versión inicial perdía los datos en silencio; la nueva informa el error y sale sin sobrescribir (prueba `test_archivo_danado_se_informa_y_no_se_sobrescribe`). Es una corrección de defecto (mejora de calidad externa), no una regresión.
