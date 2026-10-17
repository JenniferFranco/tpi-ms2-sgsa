# Etapa 2 — Calidad externa vs. calidad interna

## Calidad externa (lo que percibe el usuario) — versión inicial
| Aspecto | Observación | Evaluación |
|---|---|---|
| Funcionalidad | Las 6 operaciones hacen lo que se espera (verificado con 3 escenarios golden master). | ✅ Correcta |
| Validaciones | Mensajes claros ante legajo, email, tipo, prioridad o transición inválidos. | ✅ Correcta |
| Persistencia | Los datos sobreviven entre ejecuciones. | ✅ Correcta |
| Robustez | Si `datos.json` está dañado, el sistema arranca "vacío" sin avisar y la siguiente operación **sobrescribe el archivo**: pérdida silenciosa de datos. | ⚠️ Defecto latente |
| Usabilidad | Menú simple y consistente. | ✅ Aceptable |

## Calidad interna (lo que ve el equipo técnico) — versión inicial
| Métrica (herramienta) | Valor inicial | Lectura |
|---|---|---|
| Complejidad ciclomática promedio (radon) | 12,4 (C) | Muy por encima de lo recomendable (≤ 5). |
| Complejidad máxima | 23 (D) en `buscar()`; 21 en `cambiar_estado()` | Métodos difíciles de entender y probar. |
| Índice de mantenibilidad (radon) | 15,5 | Bajo: todo concentrado en un archivo/clase. |
| Avisos flake8 | 23 | `except:` desnudo, `== None`, varias sentencias por línea. |
| pylint | 8,57/10 — 43 avisos | bare-except, too-many-branches, consider-using-with, global-statement… |
| Pruebas automatizadas | 0 | Cambiar algo es "a ciegas". |
| Clases / responsabilidades | 1 clase hace UI + validación + reglas + persistencia + reportes | Violación directa de SRP. |

## Relación entre ambas
El sistema **funciona** (buena calidad externa), pero el **costo del cambio es alto** (mala calidad interna). Ejemplo concreto: agregar un nuevo tipo de solicitud (p. ej. "Baja de materia") obliga a modificar 5 lugares del código (validación del tipo, prioridad automática, conteo del reporte, textos de ayuda y filtro), sin pruebas que avisen si algo se rompe. La deuda interna además esconde un defecto externo (pérdida de datos con archivo dañado) que el usuario solo descubriría cuando ya es tarde.

Conclusión: la calidad externa describe el presente; la calidad interna condiciona la **evolución futura**. Por eso el foco del trabajo está en la segunda, protegida por pruebas que fijan la primera.
