# SGSA — Sistema de Gestión de Solicitudes Académicas

TPI de **Metodología de Sistemas II** — Tecnicatura Universitaria en Programación a Distancia (UTN).
Integrantes: **Jennifer Franco** y **Jonathan Franco**.

> Evolución profesional de un sistema existente: diagnóstico de calidad, deuda técnica, refactoring seguro y code review. El objetivo **no** es agregar funcionalidad sino mejorar la calidad interna sin alterar el comportamiento externo.

## Descripción
Aplicación de consola que permite registrar estudiantes y solicitudes académicas (certificados, equivalencias, mesas especiales y reclamos de nota), clasificarlas por tipo, prioridad y estado, asignar un responsable de área, buscar/filtrar y obtener un reporte básico. Los datos se guardan en un archivo JSON. Todos los datos de ejemplo son **sintéticos**.

## Funcionalidades
1. Registrar estudiante (legajo de 4-6 dígitos único, email válido).
2. Registrar solicitud (prioridad manual o automática según el tipo).
3. Cambiar estado (P→EP→R, P/EP→X; EP requiere responsable).
4. Asignar responsable (pasa la solicitud a En proceso).
5. Buscar / filtrar por estado, tipo o legajo (orden por prioridad).
6. Reporte básico (por estado, por tipo, prioridad alta abiertas, pendientes con más de 3 días).

## Tecnologías
Python 3.10+ (solo biblioteca estándar) · JSON · pytest · flake8 · pylint · radon · coverage · Git/GitHub.

## Instalación y uso
```bash
git clone https://github.com/JenniferFranco/tpi-ms2-sgsa.git
cd tpi-ms2-sgsa
python sistema.py                     # crea datos.json en la carpeta actual
SGSA_DATA=otro.json python sistema.py # (opcional) otro archivo de datos
```
En Windows (PowerShell): `$env:SGSA_DATA="otro.json"; python sistema.py`.

## Pruebas y calidad
```bash
pip install -r requirements-dev.txt
python -m pytest -v                   # 59 pruebas (3 golden master + 56 unitarias)
flake8 sistema.py sgsa tests
pylint sistema.py sgsa
radon cc -s -a sistema.py sgsa
```

## Estructura
```
sistema.py            punto de entrada
sgsa/ui/              consola y formato de salida
sgsa/servicios/       casos de uso y reporte
sgsa/dominio/         entidades, enums, reglas, validadores, excepciones
sgsa/persistencia/    repositorio abstracto, en memoria y JSON
tests/                golden master (tests/golden) + pruebas unitarias
docs/                 etapas del TPI, checklist de code review, reportes de herramientas
```

## Hitos (tags)
| Tag | Contenido |
|---|---|
| `estado-inicial` | Sistema base original (un solo archivo, con deuda técnica). |
| `etapa-diagnostico` | Pruebas golden master + diagnóstico de calidad y code smells. |
| `etapa-refactoring` | Nueva arquitectura en capas (8 refactorings documentados). |
| `etapa-pruebas` | Pruebas unitarias y evidencias. |
| `etapa-docs` | Code review aplicado, documentación final. |
| `estado-refactorizado` | Estado final del código. |

Comparar versiones: `git diff estado-inicial estado-refactorizado --stat`.

## Documentación
[Sistema base](docs/01_sistema_base.md) · [Calidad externa vs. interna](docs/02_calidad_externa_interna.md) · [Deuda técnica y code smells](docs/03_deuda_tecnica_code_smells.md) · [SOLID y Clean Code](docs/04_solid_clean_code.md) · [Refactorings](docs/05_refactorings.md) · [Pruebas](docs/06_pruebas_verificacion.md) · [Code review y checklist](docs/07_code_review.md) · [Conclusiones](docs/08_conclusiones.md) · [Uso de IA](docs/uso_ia.md)

## Participación
| Integrante | Aportes principales |
|---|---|
| Jennifer Franco | Sistema base, diagnóstico de calidad, refactoring de dominio y persistencia, revisión de servicios, UI y pruebas, correcciones CR-02 y CR-04, documentación final y conclusiones. |
| Jonathan Franco (GitHub: Yonathannf) | Golden master, code smells, refactoring de servicios y UI, pruebas unitarias, revisión de dominio y persistencia, correcciones CR-01, CR-03 y CR-05. |

## Enlaces
- Video: https://youtu.be/gMaR0jz800g
- Code review: [Pull Request #1](https://github.com/JenniferFranco/tpi-ms2-sgsa/pull/1) (observaciones) y [Pull Request #2](https://github.com/JenniferFranco/tpi-ms2-sgsa/pull/2) (correcciones CR-01, CR-03 y CR-05). Las correcciones CR-02 y CR-04 se completaron en el commit `f63701a` en main.
- Informe PDF: entregado en la plataforma.
