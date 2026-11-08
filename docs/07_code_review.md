# Etapa 7 — Code review profesional

**Modalidad:** revisión cruzada en GitHub. Las observaciones se registraron en el Pull Request #1 (refactoring, tag `etapa-pruebas`) y las correcciones se integraron en el Pull Request #2, aprobado por la otra integrante. En la verificación final se detectó que el commit de Jennifer en el PR #2 no había incluido los archivos de CR-02 y CR-04; esas correcciones se completaron en un commit posterior en `main`. Cada integrante revisó el código que **no** escribió: Jennifer revisó servicios, UI y pruebas; Jonathan revisó dominio y persistencia. Se complementó con herramientas: pylint 9,85/10 y flake8 con 6 avisos antes de la revisión (`docs/reportes/*_previo_code_review.txt`).

## Checklist técnico aplicado
| # | Categoría | Criterio | Resultado |
|---|---|---|---|
| 1 | Funcionalidad | El comportamiento externo es idéntico (golden master en verde). | ✅ |
| 2 | Funcionalidad | Los cambios de comportamiento están justificados y documentados. | ✅ (archivo dañado) |
| 3 | Diseño | Cada clase/módulo tiene una sola responsabilidad (SRP). | ✅ |
| 4 | Diseño | Las reglas se extienden sin modificar código existente (OCP). | ✅ |
| 5 | Diseño | Los servicios dependen de abstracciones (DIP); la UI no accede a la persistencia. | ✅ |
| 6 | Diseño | La UI no manipula reglas de la entidad directamente. | ⚠️ CR-03 |
| 7 | Clean Code | Nombres expresivos, sin abreviaturas crípticas. | ✅ |
| 8 | Clean Code | Funciones con complejidad ciclomática ≤ 10 y un nivel de abstracción. | ✅ (máx. 5) |
| 9 | Clean Code | Sin números/cadenas mágicas ni duplicación. | ✅ |
| 10 | Errores | Sin `except:` desnudo; excepciones específicas y con causa encadenada. | ⚠️ CR-01 |
| 11 | Estilo | flake8 sin avisos; líneas ≤ 100 caracteres. | ⚠️ CR-02 |
| 12 | Pruebas | Toda regla de negocio tiene al menos una prueba; casos límite cubiertos. | ✅ |
| 13 | Pruebas | Las pruebas son portables (Windows/Linux) y reproducibles. | ⚠️ CR-05 |
| 14 | Seguridad / privacidad | Sin datos personales reales; sin rutas ni credenciales fijas. | ✅ |
| 15 | Documentación | README y docs reflejan la nueva estructura; comentarios explican el "por qué". | ⚠️ CR-04 |

## Observaciones, feedback y acciones
| ID | Archivo | Severidad | Feedback (redactado al autor) | Acción | Estado |
|---|---|---|---|---|---|
| CR-01 | `ui/consola.py` (`leer_entero`, `leer_codigo`) | Media | "Al convertir `ValueError` en `DatoInvalidoError` se pierde la causa original. Propongo `raise … from causa` para que el traceback muestre el origen si algún día hay que depurarlo." (pylint W0707) | Se encadenaron las excepciones. | ✅ Corregido |
| CR-02 | `ui/consola.py`, `dominio/modelos.py`, pruebas | Baja | "Hay 6 líneas de más de 100 caracteres; dificultan la revisión en pantalla dividida. Sugiero variables explicativas en lugar de cortar la línea." | Se introdujeron variables explicativas (`superado`, `nombre_responsable`, `contenido`). En el PR #1 el comentario quedó anclado por error en `tests/conftest.py`; se aclaró en el hilo. | ✅ Corregido |
| CR-03 | `ui/consola.py::asignar_responsable` | Media | "La consola llama a `solicitud.verificar_que_este_abierta()` directamente: es una regla de negocio dentro de la UI. ¿Lo movemos al servicio para que cualquier otra interfaz la reutilice?" | Nuevo `ServicioSolicitudes.obtener_solicitud_abierta()`. | ✅ Corregido |
| CR-04 | `persistencia/repositorio_memoria.py::actualizar_solicitud` | Baja | "El parámetro `solicitud` parece no usarse; quien lea esto puede pensar que es un error. Vale la pena aclarar por qué." | Comentario: las entidades en memoria se modifican por referencia; solo resta persistir. | ✅ Corregido |
| CR-05 | `tests/test_persistencia_y_formato.py` | Media | "El subproceso se lanza con un entorno vacío (`env={'PATH': ''}`). En mi máquina pasa, pero sin variables como SYSTEMROOT, Python puede no iniciar en algunas versiones de Windows, y la prueba depende del entorno. Propongo heredarlo con `dict(os.environ, SGSA_DATA=…)`." | Se hereda el entorno del sistema (riesgo de portabilidad corregido de forma preventiva). | ✅ Corregido |
| CR-06 | `dominio/modelos.py::Solicitud` | Info | "pylint marca 8 atributos (máx. 7)." | **Aceptado sin cambio:** son los datos propios de la entidad; dividirla agregaría complejidad sin beneficio. | ✅ Aceptado con justificación |
| CR-07 | `servicios/servicio_reportes.py::ReporteBasico` | Info | "pylint marca *too-few-public-methods*." | **Falso positivo:** es un `dataclass` de solo datos. | ✅ Aceptado |
| CR-08 | `servicios/servicio_solicitudes.py::FiltroSolicitudes` | Baja | "El filtro usa códigos `str` en vez de los enums: queda un resto de *primitive obsession*." | **Decisión consciente:** con un código inexistente (p. ej. estado `Z`) la versión inicial muestra "No se encontraron solicitudes"; convertir a enum cambiaría ese comportamiento. Se registra como mejora futura. | 🕒 Diferido (documentado) |

## Criterios de aceptación técnica (Definition of Done del refactoring)
- [x] 59/59 pruebas en verde, incluidas las 3 golden master sin modificar.
- [x] flake8: 0 avisos (`--max-line-length=100`).
- [x] pylint ≥ 9,5 → **9,96/10**; los avisos restantes están justificados (CR-06, CR-07).
- [x] Complejidad ciclomática ≤ 10 por función → máximo 5.
- [x] Ningún `except:` desnudo ni variable global mutable.
- [x] Formato de `datos.json` compatible con la versión inicial.
- [x] README y `/docs` actualizados; observaciones del review resueltas o justificadas.
- [x] Aprobación del Pull Request por el otro integrante.
