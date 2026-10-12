"""Pruebas de caracterizacion (golden master).

Ejecutan el sistema completo (`python sistema.py`) alimentando el menu con
guiones de entrada fijos y comparan la salida de consola y el archivo de datos
resultante contra una "salida aprobada" generada con la version inicial
(tag estado-inicial). Si un refactoring cambia el comportamiento externo,
estas pruebas fallan.

Para regenerar las salidas aprobadas (solo sobre la version inicial):
    SGSA_APROBAR=1 python -m pytest tests/test_golden_master.py
"""
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent
GOLDEN = Path(__file__).resolve().parent / "golden"
APROBAR = os.environ.get("SGSA_APROBAR") == "1"

# (nombre, [(guion de entrada, fecha simulada), ...]) -> los pasos comparten archivo de datos
ESCENARIOS = [
    ("esc01_alta_y_flujo", [("esc01_alta_y_flujo.txt", "2026-10-12")]),
    ("esc02_validaciones", [("esc02_validaciones.txt", "2026-10-12")]),
    ("esc03_reporte_vencidas", [
        ("esc03a_carga_previa.txt", "2026-10-01"),
        ("esc03b_reporte_posterior.txt", "2026-10-12"),
    ]),
]


def ejecutar(guion: str, fecha: str, archivo_datos: Path) -> str:
    entorno = dict(os.environ, SGSA_DATA=str(archivo_datos), SGSA_HOY=fecha)
    entrada = (GOLDEN / guion).read_text(encoding="utf-8")
    resultado = subprocess.run(
        [sys.executable, "sistema.py"], cwd=RAIZ, input=entrada,
        capture_output=True, text=True, env=entorno, timeout=30,
    )
    assert resultado.returncode == 0, resultado.stderr
    return resultado.stdout


@pytest.mark.parametrize("nombre,pasos", ESCENARIOS, ids=[e[0] for e in ESCENARIOS])
def test_comportamiento_externo_se_mantiene(nombre, pasos, tmp_path):
    archivo_datos = tmp_path / "datos.json"
    salida = "".join(ejecutar(g, f, archivo_datos) for g, f in pasos)
    datos_finales = json.loads(archivo_datos.read_text(encoding="utf-8")) if archivo_datos.exists() else None

    esperado_txt = GOLDEN / f"{nombre}.salida.txt"
    esperado_json = GOLDEN / f"{nombre}.datos.json"
    if APROBAR:
        esperado_txt.write_text(salida, encoding="utf-8")
        esperado_json.write_text(json.dumps(datos_finales, indent=2, ensure_ascii=False), encoding="utf-8")
        pytest.skip("salida aprobada regenerada")

    assert salida == esperado_txt.read_text(encoding="utf-8")
    assert datos_finales == json.loads(esperado_json.read_text(encoding="utf-8"))
