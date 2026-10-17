# Etapa 3 — Deuda técnica y code smells

Ubicaciones referidas a `sistema.py` en el tag `estado-inicial`. Prioridad: **Alta** = corregir primero (riesgo de defecto o bloquea otros cambios); **Media** = corregir en este ciclo; **Baja** = mejora oportunista.

| ID | Smell / debilidad | Evidencia y ubicación | Impacto | Riesgo de mantenimiento | Prioridad |
|---|---|---|---|---|---|
| CS-01 | **God Class** (Large Class) | `GestorSolicitudes` (L31-297) hace entrada/salida, validación, reglas, persistencia y reportes. | Cualquier cambio toca la misma clase; imposible reutilizar o probar partes aisladas. | Alto | Alta |
| CS-02 | **Long Method** | `buscar()` L197-249 (CC 23), `cambiar_estado()` L111-155 (CC 21), `reporte()` L251-297 (CC 20), `registrar_solicitud()` L59-98 (CC 19). | Difíciles de leer; mezclan niveles de abstracción. | Alto | Alta |
| CS-03 | **Duplicated Code** | Validación de legajo ×3 (L37, L63, L214); escritura del JSON ×4 (L54, L105, L144, L192); búsqueda de solicitud por id ×2 (L118-121, L164-167); traducción código→texto de estado ×2 (L147-154, L231-238). | Un cambio de regla hay que replicarlo a mano; fácil olvidar uno. | Alto | Alta |
| CS-04 | **Long Parameter List** + parámetros sin uso | `crear_solicitud()` con 9 parámetros (L100); `nombre` y `email` no se usan (lo admite el comentario de L108). | Llamadas frágiles: es fácil invertir argumentos posicionales. | Medio | Media |
| CS-05 | **Primitive Obsession / números y cadenas mágicas** | Estados `"P"`, `"EP"`, `"R"`, `"X"`; prioridades `1/2/3`; `3` días (L293); 4/6 dígitos; 10 caracteres; solicitudes como `dict`. | El significado está implícito; un error de tipeo (`"Ep"`) no lo detecta nadie. | Alto | Alta |
| CS-06 | **Switch Statements** (cadenas if/elif) — viola OCP | Prioridad automática (L84-92); transiciones con `flag` (L130-139); contadores `c1..c4` / `t1..t4` (L262-284). | Agregar un tipo o estado obliga a modificar código existente en varios lugares. | Medio | Media |
| CS-07 | **Manejo de errores deficiente** | 5 `except:` desnudos (L15, L115, L161, L178, L258); errores como `print()` + `return`; archivos abiertos sin `with`. L15 oculta un JSON dañado → se arranca vacío y se pisan los datos. | Errores silenciosos y **pérdida de datos**; la lógica no se puede probar sin leer la consola. | Alto | Alta |
| CS-08 | **Estado global + acoplamiento a la persistencia concreta** (viola DIP) | Variable global `datos` (L6, L10); `open(DATA_FILE)` dentro de la lógica de negocio. | Imposible probar sin archivo real; cambiar a base de datos implica reescribir todo. | Alto | Alta |
| CS-09 | **Nombres poco expresivos** | `d`, `p`, `t`, `n`, `a`, `em`, `x`, `s`, `v`, `rn`, `flag`, `c1..c4`; `id` oculta un builtin (L114, L160). | Obliga a leer todo el contexto para entender una línea. | Medio | Media |
| CS-10 | **Comentarios que justifican código / fuente de verdad duplicada** | "leemos de nuevo el archivo por las dudas" (L253): `reporte()` relee el disco en vez de usar el estado en memoria. Cabecera "hecho rápido… después lo ordenamos". | Dos fuentes de verdad que podrían divergir; deuda reconocida pero no gestionada. | Bajo | Baja |

## Clasificación de la deuda (cuadrante de Fowler)
La mayor parte es **deliberada e imprudente** ("hecho rápido para la demo, después lo ordenamos"): se sabía que se tomaba un atajo y no se planificó pagarlo. CS-07 (pérdida de datos) es además **inadvertida**: nadie la había detectado.

## Orden de corrección elegido
1. Red de seguridad: pruebas de caracterización (golden master) **antes** de tocar el código.
2. CS-05 y CS-06 (tipos y reglas) → base para mover comportamiento al dominio.
3. CS-08 y CS-01 (persistencia y separación de capas).
4. CS-02, CS-03, CS-04, CS-07, CS-09 (métodos, duplicación, parámetros, errores, nombres).
5. CS-10 se resuelve como efecto de la nueva arquitectura (una sola fuente de verdad: el repositorio).
