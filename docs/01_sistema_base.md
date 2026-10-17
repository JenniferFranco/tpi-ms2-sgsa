# Etapa 1 — Selección y descripción del sistema base

## Dominio y alcance
**SGSA — Sistema de Gestión de Solicitudes Académicas** (caso sugerido por la cátedra). Aplicación de consola en Python que permite registrar estudiantes y sus solicitudes académicas, clasificarlas por tipo, prioridad y estado, asignar un responsable, buscar/filtrar y emitir un reporte básico.

Alcance del TPI: **no agregar funcionalidad**, sino diagnosticar y mejorar la calidad interna del módulo completo manteniendo el comportamiento externo.

## Actores
| Actor | Descripción |
|---|---|
| Operador administrativo | Usa el sistema: registra estudiantes y solicitudes, asigna, cambia estados, consulta. |
| Responsable de área | Alumnado, Secretaría Académica o Bedelía. Se le asignan solicitudes (precargados). |
| Estudiante | Origen de la solicitud (no opera el sistema). |

## Entidades (≥ 3)
Estudiante · Responsable/Área · Solicitud · Estado · (TipoSolicitud y Prioridad).

## Operaciones funcionales verificables (≥ 4)
| # | Operación | Regla de negocio principal |
|---|---|---|
| 1 | Registrar estudiante | Legajo numérico de 4 a 6 dígitos, único; nombre y apellido obligatorios; email válido. |
| 2 | Registrar solicitud | El estudiante debe existir; tipo CERT/EQUIV/MESA/RECL; descripción ≥ 10 caracteres; prioridad manual o automática según el tipo. |
| 3 | Cambiar estado | Transiciones válidas: P→EP, P→X, EP→R, EP→X. Para pasar a EP debe haber responsable. |
| 4 | Asignar responsable | No se asigna a solicitudes cerradas (R/X). Si estaba Pendiente pasa a En proceso. |
| 5 | Buscar / filtrar | Por estado, tipo, legajo o todas; ordenado por prioridad y número. |
| 6 | Reporte básico | Totales por estado y tipo, abiertas de prioridad alta y pendientes con más de 3 días sin atender. |

## Tecnología
Python 3.10+ (sin dependencias de ejecución) · persistencia en archivo JSON (`datos.json`, configurable con `SGSA_DATA`) · pytest, flake8, pylint, radon y coverage para verificación · Git/GitHub.

## Versión inicial
Tag `estado-inicial`: un único archivo `sistema.py` (334 líneas) con una clase `GestorSolicitudes`. Funciona correctamente, pero fue escrito "rápido para la demo" y acumula deuda técnica deliberada (ver etapa 3).

Datos utilizados: **sintéticos** (nombres y legajos inventados), según la consigna.
