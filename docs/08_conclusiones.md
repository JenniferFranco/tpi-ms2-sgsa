# Etapa 8 — Conclusiones y aprendizaje

## Resultados medibles
| Indicador | estado-inicial | estado-refactorizado |
|---|---|---|
| Complejidad ciclomática promedio | 12,4 (C) | 1,9 (A) |
| Complejidad máxima | 23 (D) | 5 (A) |
| pylint | 8,57/10 (43 avisos) | 9,96/10 (2 avisos justificados) |
| flake8 | 23 avisos | 0 |
| Pruebas automatizadas | 0 | 59 (cobertura 92 % del paquete) |
| Archivos / clases | 1 / 1 | 14 módulos / 20 clases (incluye enums y excepciones) |
| Líneas de código | 334 | 765 |
| Comportamiento externo | — | Idéntico (golden master) + 1 defecto corregido |

## Decisiones tomadas
- Escribir pruebas de caracterización **antes** del primer cambio: sin ellas no hay refactoring "seguro", solo reescritura.
- Construir la nueva estructura en paralelo y conectar la UI al final, para que cada commit quede funcionando.
- Mantener textos de consola y formato JSON idénticos para poder comparar antes/después de forma automática.
- No aplicar ISP de forma forzada ni convertir el filtro a enums (CR-08): mejorar la calidad también es saber dónde **no** tocar.

## Dificultades
- Mantener la salida **carácter por carácter** igual obligó a respetar el orden exacto en que la versión inicial pedía datos y mostraba errores.
- Las fechas hacían que las pruebas no fueran reproducibles: se resolvió con la variable `SGSA_HOY`.
- Decidir qué hacer con el archivo dañado: preservar el comportamiento implicaba preservar un defecto; se eligió corregirlo y documentarlo como única diferencia.

## Límites del trabajo
- La cantidad de líneas creció (334 → 765): más archivos pequeños y legibles en lugar de uno grande. Se prioriza el costo de **cambio**, no el de escritura.
- El sistema sigue siendo de consola y monousuario; el JSON no soporta concurrencia.
- La UI no se mide en la cobertura porque se prueba por subproceso.

## Mejoras futuras
- Reemplazar `RepositorioJSON` por SQLite sin tocar servicios (gracias a DIP).
- Convertir `FiltroSolicitudes` a enums cuando se acepte el cambio de mensaje (CR-08).
- Historial de cambios de estado por solicitud y notificación por email al estudiante.
- Integración continua (GitHub Actions) ejecutando pytest + flake8 en cada push, y pre-commit.

## Relación con la asignatura
Calidad externa vs. interna (etapa 2), deuda técnica y cuadrante de Fowler (etapa 3), SOLID y Clean Code (etapa 4), catálogo de refactorings (etapa 5), pruebas de regresión y valores límite (etapa 6), code review con checklist y Definition of Done (etapa 7), y Git con tags por hito como soporte de trazabilidad.

## Conclusiones individuales
**Jennifer Franco:** Mi tarea principal fue ocuparme del sistema base, el diagnóstico de calidad, el refactoring del dominio y la persistencia, y la revisión del código de servicios, interfaz y pruebas. La mayor conclusión que me llevo es que es sumamente útil escribir las pruebas golden master antes de tocar el código, porque permiten refactorizar con tranquilidad: cada commit se podía verificar en segundos. También aprendí que el code review sirve para detectar riesgos y no solo errores visibles, como en el CR-05, donde la prueba pasaba en mi máquina pero era frágil. Y que hay que verificar lo que realmente se sube: en la revisión final descubrimos que uno de mis commits no incluía los archivos de las correcciones CR-02 y CR-04, lo que me llevó a aprender que siempre voy a correr `git show --stat` antes de abrir o aprobar un Pull Request.

**Jonathan Franco:** Me ofrecí a ocuparme de las pruebas golden master, el análisis de code smells, el refactoring de servicios e interfaz, las pruebas unitarias y la revisión del dominio y la persistencia. La mayor enseñanza que me llevo fue construir la nueva arquitectura en paralelo y conectar la interfaz recién al final: así el sistema nunca dejó de funcionar. En el code review aprendí a defender decisiones de no cambiar, como el CR-08, cuando corregir algo alteraría el comportamiento externo. Como mejora, unimos el primer Pull Request antes de aplicar las correcciones y las tuvimos que integrar en un segundo PR; nos dimos cuenta de que la próxima vez hay que esperar a que la revisión esté cerrada y aprobada antes del merge, aunque también aprendimos que todo problema es solucionable.
