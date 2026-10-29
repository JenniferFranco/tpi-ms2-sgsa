import json
import subprocess
import sys
from pathlib import Path

from sgsa.dominio.enums import Estado
from sgsa.persistencia.repositorio_json import RepositorioJSON
from sgsa.ui import formato

GOLDEN = Path(__file__).resolve().parent / "golden"
RAIZ = Path(__file__).resolve().parent.parent


def test_lee_archivos_generados_por_la_version_inicial(tmp_path):
    # Compatibilidad hacia atras: el formato JSON no cambio con el refactoring.
    archivo = tmp_path / "datos.json"
    archivo.write_text((GOLDEN / "esc01_alta_y_flujo.datos.json").read_text(encoding="utf-8"))
    repo = RepositorioJSON(str(archivo))
    assert repo.buscar_solicitud(1).estado is Estado.RESUELTA
    assert repo.buscar_estudiante("20511").apellido == "Lopez"


def test_guardar_y_releer_produce_el_mismo_contenido(tmp_path):
    archivo = tmp_path / "datos.json"
    original = (GOLDEN / "esc03_reporte_vencidas.datos.json").read_text(encoding="utf-8")
    archivo.write_text(original)
    repo = RepositorioJSON(str(archivo))
    repo.actualizar_solicitud(repo.buscar_solicitud(1))  # fuerza una escritura
    assert json.loads(archivo.read_text()) == json.loads(original)


def test_archivo_inexistente_no_se_crea_hasta_la_primera_escritura(tmp_path):
    archivo = tmp_path / "nuevo.json"
    repo = RepositorioJSON(str(archivo))
    assert len(repo.listar_responsables()) == 3 and not archivo.exists()


def test_archivo_danado_se_informa_y_no_se_sobrescribe(tmp_path):
    # Mejora intencional: la version inicial ocultaba el error (except: pass)
    # y terminaba pisando el archivo con datos vacios.
    archivo = tmp_path / "datos.json"
    archivo.write_text("{ esto no es json")
    resultado = subprocess.run([sys.executable, "sistema.py"], cwd=RAIZ, input="0\n",
                               capture_output=True, text=True,
                               env={"SGSA_DATA": str(archivo), "PATH": ""})
    assert resultado.returncode == 1
    assert "archivo de datos esta danado" in resultado.stdout
    assert archivo.read_text() == "{ esto no es json"


def test_formato_de_fila_sin_responsable(tmp_path):
    archivo = tmp_path / "datos.json"
    archivo.write_text((GOLDEN / "esc03_reporte_vencidas.datos.json").read_text(encoding="utf-8"))
    s = RepositorioJSON(str(archivo)).buscar_solicitud(2)
    assert formato.fila_solicitud(s, None) == \
        "#2 | CERT | Pendiente | Prioridad: Baja | Legajo: 30001 | Resp: -"
