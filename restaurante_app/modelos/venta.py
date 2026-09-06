class Venta:
    def __init__(self, usuario_id: str, producto_codigo: str, cantidad: int = 1) -> None:
        self._usuario_id = ""
        self._producto_codigo = ""
        self._cantidad = 1

        self.usuario_id = usuario_id
        self.producto_codigo = producto_codigo
        self.cantidad = cantidad

    @property
    def usuario_id(self) -> str:
        return self._usuario_id

    @usuario_id.setter
    def usuario_id(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El ID de usuario no puede estar vacío.")
        self._usuario_id = valor.strip()

    @property
    def producto_codigo(self) -> str:
        return self._producto_codigo

    @producto_codigo.setter
    def producto_codigo(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El código de producto no puede estar vacío.")
        self._producto_codigo = valor.strip()

    @property
    def cantidad(self) -> int:
        return self._cantidad

    @cantidad.setter
    def cantidad(self, valor: int) -> None:
        try:
            val_entero = int(valor)
        except (TypeError, ValueError):
            raise ValueError("La cantidad de venta debe ser un número entero.")
        if val_entero <= 0:
            raise ValueError("La cantidad vendida debe ser mayor a cero.")
        self._cantidad = val_entero

    def convertir_a_diccionario(self) -> dict:
        return {
            "usuario_id": self._usuario_id,
            "producto_codigo": self._producto_codigo,
            "cantidad": self._cantidad,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Venta":
        return cls(
            usuario_id=data["usuario_id"],
            producto_codigo=data["producto_codigo"],
            cantidad=data["cantidad"],
        )

    def __str__(self) -> str:
        return (
            f"Venta -> Usuario: {self._usuario_id} | "
            f"Producto: {self._producto_codigo} | Cantidad: {self._cantidad}"
        )