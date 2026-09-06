class Producto:
    def __init__(
        self,
        codigo: str,
        nombre: str,
        precio: float,
        stock: int = 0,
        categoria: str = "General",
    ) -> None:
        self._codigo = ""
        self._nombre = ""
        self._precio = 0.0
        self._stock = 0
        self._categoria = "General"

        self.codigo = codigo
        self.nombre = nombre
        self.precio = precio
        self.stock = stock
        self.categoria = categoria

    @property
    def codigo(self) -> str:
        return self._codigo

    @codigo.setter
    def codigo(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El código del producto no puede estar vacío.")
        self._codigo = valor.strip()

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El nombre del producto no puede estar vacío.")
        self._nombre = valor.strip()

    @property
    def precio(self) -> float:
        return self._precio

    @precio.setter
    def precio(self, valor: float) -> None:
        try:
            val_flotante = float(valor)
        except (TypeError, ValueError):
            raise ValueError("El precio debe ser un número válido.")
        if val_flotante < 0:
            raise ValueError("El precio no puede ser negativo.")
        self._precio = val_flotante

    @property
    def stock(self) -> int:
        return self._stock

    @stock.setter
    def stock(self, valor: int) -> None:
        try:
            val_entero = int(valor)
        except (TypeError, ValueError):
            raise ValueError("El stock debe ser un número entero.")
        if val_entero < 0:
            raise ValueError("El stock no puede ser negativo.")
        self._stock = val_entero

    @property
    def categoria(self) -> str:
        return self._categoria

    @categoria.setter
    def categoria(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("La categoría no puede estar vacía.")
        self._categoria = valor.strip().title()

    def vender(self, cantidad: int = 1) -> bool:
        if cantidad <= 0 or self._stock < cantidad:
            return False
        self._stock -= cantidad
        return True

    def convertir_a_diccionario(self) -> dict:
        return {
            "codigo": self._codigo,
            "nombre": self._nombre,
            "precio": self._precio,
            "stock": self._stock,
            "categoria": self._categoria,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Producto":
        return cls(
            codigo=data["codigo"],
            nombre=data["nombre"],
            precio=data["precio"],
            stock=data.get("stock", 0),
            categoria=data.get("categoria", "General"),
        )

    def __str__(self) -> str:
        return (
            f"[{self._codigo}] {self._nombre} ({self._categoria}) "
            f"- ${self._precio:.2f} | Stock: {self._stock}"
        )