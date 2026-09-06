import json
from pathlib import Path
from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta

class ArchivoServicio:
    def __init__(self, ruta_base: str = "datos") -> None:
        self._directorio = Path(ruta_base)
        self._ruta_productos = self._directorio / "productos.json"
        self._ruta_usuarios = self._directorio / "usuarios.json"
        self._ruta_ventas = self._directorio / "ventas.json"

    def _guardar_lista(self, ruta: Path, datos: list, nombre: str) -> bool:
        try:
            ruta.parent.mkdir(parents=True, exist_ok=True)
            with open(ruta, "w", encoding="utf-8") as archivo:
                json.dump(datos, archivo, indent=4, ensure_ascii=False)
            return True
        except PermissionError:
            print(f"Error: Sin permisos para guardar en el archivo de {nombre}.")
            return False

    def _leer_lista(self, ruta: Path, nombre: str) -> list:
        try:
            with open(ruta, "r", encoding="utf-8") as archivo:
                return json.load(archivo)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            print(f"Advertencia: El archivo de {nombre} contiene un JSON inválido. Se inicia con colección vacía.")
            return []
        except PermissionError:
            print(f"Error: Permiso denegado para leer el archivo de {nombre}.")
            return []

    # Persistencia de Productos
    def guardar_productos(self, productos: list[Producto]) -> bool:
        datos = [p.convertir_a_diccionario() for p in productos]
        return self._guardar_lista(self._ruta_productos, datos, "productos")

    def cargar_productos(self) -> list[Producto]:
        datos = self._leer_lista(self._ruta_productos, "productos")
        productos: list[Producto] = []
        for item in datos:
            try:
                productos.append(Producto.from_dict(item))
            except (KeyError, ValueError) as error:
                print(f"Omitiendo registro de producto defectuoso: {error}")
        return productos

    # Persistencia de Usuarios
    def guardar_usuarios(self, usuarios: list[Usuario]) -> bool:
        datos = [u.convertir_a_diccionario() for u in usuarios]
        return self._guardar_lista(self._ruta_usuarios, datos, "usuarios")

    def cargar_usuarios(self) -> list[Usuario]:
        datos = self._leer_lista(self._ruta_usuarios, "usuarios")
        usuarios: list[Usuario] = []
        for item in datos:
            try:
                usuarios.append(Usuario.from_dict(item))
            except (KeyError, ValueError) as error:
                print(f"Omitiendo registro de usuario defectuoso: {error}")
        return usuarios

    # Persistencia de Ventas
    def guardar_ventas(self, ventas: list[Venta]) -> bool:
        datos = [v.convertir_a_diccionario() for v in ventas]
        return self._guardar_lista(self._ruta_ventas, datos, "ventas")

    def cargar_ventas(self) -> list[Venta]:
        datos = self._leer_lista(self._ruta_ventas, "ventas")
        ventas: list[Venta] = []
        for item in datos:
            try:
                ventas.append(Venta.from_dict(item))
            except (KeyError, ValueError) as error:
                print(f"Omitiendo registro de venta defectuoso: {error}")
        return ventas