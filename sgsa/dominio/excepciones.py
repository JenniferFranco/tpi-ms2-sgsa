"""Excepciones de negocio: reemplazan los print + return silenciosos."""


class ErrorSGSA(Exception):
    """Error de negocio cuyo mensaje se muestra tal cual al usuario."""


class DatoInvalidoError(ErrorSGSA):
    pass


class EntidadNoEncontradaError(ErrorSGSA):
    pass


class EntidadDuplicadaError(ErrorSGSA):
    pass


class OperacionNoPermitidaError(ErrorSGSA):
    pass
