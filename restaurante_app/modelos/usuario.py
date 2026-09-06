class Usuario:
    def __init__(self, identificacion: str, nombre: str) -> None:
        self._identificacion = ""
        self._nombre = ""

        self.identificacion = identificacion
        self.nombre = nombre

    @property
    def identificacion(self) -> str:
        return self._identificacion

    @identificacion.setter
    def identificacion(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("La identificación del usuario no puede estar vacía.")
        self._identificacion = valor.strip()

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El nombre del usuario no puede estar vacío.")
        self._nombre = valor.strip()

    def convertir_a_diccionario(self) -> dict:
        return {
            "identificacion": self._identificacion,
            "nombre": self._nombre,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Usuario":
        return cls(
            identificacion=data["identificacion"],
            nombre=data["nombre"],
        )

    def __str__(self) -> str:
        return f"Usuario ID: {self._identificacion} | Nombre: {self._nombre}"