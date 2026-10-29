# Etapa 6 — Pruebas y verificación del comportamiento

## Estrategia en dos niveles
1. **Pruebas de caracterización (golden master)** — `tests/test_golden_master.py`. Ejecutan el programa completo (`python sistema.py`) con guiones de entrada fijos y comparan la salida de consola **y** el archivo JSON resultante contra la "salida aprobada" generada con la versión inicial. Son la red de seguridad del refactoring: no dependen de la estructura interna, por eso pudieron escribirse **antes** de refactorizar y siguieron sin cambios hasta el final.
2. **Pruebas unitarias** — dominio, validadores, servicios (con repositorio en memoria gracias a DIP) y persistencia. Documentan las reglas de negocio y permiten detectar errores en el lugar exacto.

La fecha se controla con la variable `SGSA_HOY` y el archivo con `SGSA_DATA`, para que las pruebas sean reproducibles.

## Escenarios golden master
| ID | Escenario | Qué cubre |
|---|---|---|
| GM-01 | `esc01_alta_y_flujo` | Alta de 2 estudiantes y 3 solicitudes (prioridad automática y manual), asignación (P→EP automática), transición no permitida EP→EP, resolución, listado completo y reporte. |
| GM-02 | `esc02_validaciones` | Todos los mensajes de error: legajo inválido/duplicado, nombre vacío, email, estudiante inexistente, tipo, descripción corta, prioridad, número inválido, solicitud/responsable inexistente, estado inválido, transición P→R, EP sin responsable, asignar a cerrada, filtros sin resultados, opciones inválidas. |
| GM-03 | `esc03_reporte_vencidas` | Dos ejecuciones con fechas distintas (01/10 y 12/10): persistencia entre sesiones y cálculo de pendientes con más de 3 días. |

## Catálogo de casos de prueba (resumen)
| ID | Caso | Entrada / condición | Resultado esperado | Prueba automatizada |
|---|---|---|---|---|
| CP-01 | Legajo válido/inválido | `1234`, `123456`, `00000` / `123`, `1234567`, `12a4`, `-1234`, vacío | Acepta / "legajo invalido (4 a 6 digitos)" | `test_legajos_validos`, `test_legajos_invalidos` |
| CP-02 | Email | `ana@mail.com` / `ana.mail.com`, `ana@mail` | Acepta / "email invalido" | `test_emails_*` |
| CP-03 | Descripción (valor límite) | 10 caracteres / 9 caracteres | Acepta / error | `test_descripcion_limite_diez_caracteres` |
| CP-04 | Legajo duplicado | Registrar `10234` dos veces | `EntidadDuplicadaError` | `test_no_se_registra_legajo_duplicado` |
| CP-05 | Prioridad automática | RECL, MESA, EQUIV, CERT | Alta, Alta, Media, Baja | `test_prioridad_automatica_por_tipo` |
| CP-06 | Transiciones permitidas | P→X, EP→R, EP→X | Cambia el estado | `test_transiciones_permitidas` |
| CP-07 | Transiciones prohibidas | P→R, EP→P, R→EP, X→P | "transicion no permitida" | `test_transiciones_no_permitidas` |
| CP-08 | EP sin responsable | P→EP sin asignar | "debe asignar un responsable antes" | `test_pasar_a_en_proceso_requiere_responsable` |
| CP-09 | Asignación | Asignar a pendiente / a cerrada / responsable 9 | Pasa a EP / "ya esta cerrada" / "el responsable no existe" sin cambiar estado | `test_asignar_*`, `test_no_se_*` |
| CP-10 | Búsqueda y orden | 3 solicitudes con prioridades distintas | Orden por prioridad e id: `[2, 1, 3]` | `test_busqueda_filtra_y_ordena_por_prioridad_e_id` |
| CP-11 | Vencimiento (valor límite) | Pendiente desde 01/10, hoy 04/10 y 05/10 | 3 días: no vencida · 4 días: vencida | `test_vencimiento_es_mayor_a_tres_dias` |
| CP-12 | Reporte | 3 solicitudes, 1 asignada, 1 vencida | Conteos correctos | `test_reporte_cuenta_por_estado_tipo_y_vencidas` |
| CP-13 | Compatibilidad de datos | `datos.json` generado por la versión inicial | Se lee sin cambios | `test_lee_archivos_generados_por_la_version_inicial` |
| CP-14 | Archivo dañado | JSON inválido | Mensaje claro, código de salida 1, archivo intacto | `test_archivo_danado_se_informa_y_no_se_sobrescribe` |
| CP-15 | Comportamiento externo completo | Escenarios GM-01 a GM-03 | Salida y datos idénticos a la versión inicial | `test_comportamiento_externo_se_mantiene` |

## Resultados
| Versión | Pruebas | Resultado |
|---|---|---|
| `estado-inicial` + golden master | 3 | 3 aprobadas |
| `estado-refactorizado` | 59 (3 golden + 56 unitarias) | 59 aprobadas |
| Cobertura de `sgsa/` (coverage) | — | 92 % (la UI se ejercita por subproceso en el golden master y no suma al porcentaje) |

Evidencias: `docs/reportes/pytest_inicial.txt`, `pytest_refactorizado.txt`, `coverage_refactorizado.txt`.

## Cómo reproducir
```bash
python -m pytest -v                       # todas las pruebas
git checkout estado-inicial && python -m pytest tests/test_golden_master.py   # (desde etapa-diagnostico)
```
