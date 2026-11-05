import pytest

from sgsa.dominio.excepciones import DatoInvalidoError
from sgsa.dominio.validadores import (validar_descripcion, validar_email, validar_legajo,
                                      validar_nombre_completo)


@pytest.mark.parametrize("legajo", ["1234", "123456", "00000"])
def test_legajos_validos(legajo):
    assert validar_legajo(legajo) == legajo


@pytest.mark.parametrize("legajo", ["123", "1234567", "12a4", "", "-1234"])
def test_legajos_invalidos(legajo):
    with pytest.raises(DatoInvalidoError, match="legajo invalido"):
        validar_legajo(legajo)


@pytest.mark.parametrize("email", ["ana@mail.com", "a.b@uni.edu.ar"])
def test_emails_validos(email):
    assert validar_email(email) == email


@pytest.mark.parametrize("email", ["ana.mail.com", "ana@mail", ""])
def test_emails_invalidos(email):
    with pytest.raises(DatoInvalidoError):
        validar_email(email)


def test_nombre_y_apellido_obligatorios():
    with pytest.raises(DatoInvalidoError):
        validar_nombre_completo("", "Gomez")


def test_descripcion_limite_diez_caracteres():
    assert validar_descripcion("x" * 10)
    with pytest.raises(DatoInvalidoError):
        validar_descripcion("x" * 9)
