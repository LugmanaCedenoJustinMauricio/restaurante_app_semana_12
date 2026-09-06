from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta

class Restaurante:
    def __init__(
        self,
        productos: list[Producto] | None = None,
        usuarios: list[Usuario] | None = None,
        ventas: list[Venta] | None = None,
    ) -> None:
        # Colecciones principales (Conservan la secuencia y persistencia)
        self._productos: list[Producto] = list(productos) if productos is not None else []
        self._usuarios: list[Usuario] = list(usuarios) if usuarios is not None else []
        self._ventas: list[Venta] = list(ventas) if ventas is not None else []

        # Estructuras auxiliares en memoria (Índices para optimización O(1))
        self._productos_por_codigo: dict[str, Producto] = {}
        self._usuarios_por_identificacion: dict[str, Usuario] = {}
        self._ventas_por_usuario: dict[str, list[Venta]] = {}
        self._categorias: set[str] = set()
        self._usuarios_con_compras: set[str] = set()

        # Reconstrucción inicial de índices desde los datos persistidos
        self._reconstruir_indices()

    # Reconstrucción de estructuras auxiliares
    def _reconstruir_indices(self) -> None:
        self._productos_por_codigo.clear()
        self._usuarios_por_identificacion.clear()
        self._ventas_por_usuario.clear()
        self._categorias.clear()
        self._usuarios_con_compras.clear()

        for prod in self._productos:
            self._productos_por_codigo[prod.codigo.lower()] = prod
            self._categorias.add(prod.categoria)

        for usu in self._usuarios:
            self._usuarios_por_identificacion[usu.identificacion.lower()] = usu

        for venta in self._ventas:
            uid = venta.usuario_id.lower()
            self._ventas_por_usuario.setdefault(uid, []).append(venta)
            self._usuarios_con_compras.add(uid)

    # Búsquedas directas O(1) mediante índices
    def buscar_producto(self, codigo: str) -> Producto | None:
        return self._productos_por_codigo.get(codigo.strip().lower())

    def buscar_usuario(self, identificacion: str) -> Usuario | None:
        return self._usuarios_por_identificacion.get(identificacion.strip().lower())

    # Métodos basados en conjuntos (set) para pertenencia y unicidad
    def obtener_categorias_unicas(self) -> set[str]:
        return self._categorias.copy()

    def existe_categoria(self, categoria: str) -> bool:
        return categoria.strip().title() in self._categorias

    def usuario_tiene_compras(self, identificacion: str) -> bool:
        return identificacion.strip().lower() in self._usuarios_con_compras

    # Registro y sincronización atómica
    def agregar_producto(self, producto: Producto) -> bool:
        clave = producto.codigo.lower()
        if clave in self._productos_por_codigo:
            return False

        # Actualización coordinada: lista principal e índices
        self._productos.append(producto)
        self._productos_por_codigo[clave] = producto
        self._categorias.add(producto.categoria)
        return True

    def agregar_usuario(self, usuario: Usuario) -> bool:
        clave = usuario.identificacion.lower()
        if clave in self._usuarios_por_identificacion:
            return False

        # Actualización coordinada: lista principal e índice
        self._usuarios.append(usuario)
        self._usuarios_por_identificacion[clave] = usuario
        return True

    # Operación de Venta optimizada
    def vender_producto(
        self, codigo_producto: str, identificacion_usuario: str, cantidad: int = 1
    ) -> bool:
        # Búsqueda O(1) en los índices de memoria
        usuario = self.buscar_usuario(identificacion_usuario)
        producto = self.buscar_producto(codigo_producto)

        if usuario is None or producto is None:
            return False

        if cantidad <= 0 or producto.stock < cantidad:
            return False

        venta = Venta(usuario.identificacion, producto.codigo, cantidad)
        
        # Sincronización de colección principal e índices de agrupación
        self._ventas.append(venta)
        uid = usuario.identificacion.lower()
        self._ventas_por_usuario.setdefault(uid, []).append(venta)
        self._usuarios_con_compras.add(uid)

        producto.vender(cantidad)
        return True

    # Consulta optimizada O(1) de ventas por usuario
    def consultar_ventas_usuario(self, identificacion_usuario: str) -> list[Venta]:
        uid = identificacion_usuario.strip().lower()
        # Retorna copia de la lista agrupada sin recorrer toda la colección de ventas
        return self._ventas_por_usuario.get(uid, []).copy()

    # Getters que preservan encapsulamiento
    def obtener_productos(self) -> list[Producto]:
        return list(self._productos)

    def obtener_usuarios(self) -> list[Usuario]:
        return list(self._usuarios)

    def obtener_ventas(self) -> list[Venta]:
        return list(self._ventas)