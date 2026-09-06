from modelos.producto import Producto
from modelos.usuario import Usuario
from servicios.archivo_servicio import ArchivoServicio
from servicios.restaurante import Restaurante

def pedir_texto(mensaje: str) -> str:
    return input(mensaje).strip()

def pedir_entero(mensaje: str) -> int:
    while True:
        entrada = input(mensaje).strip()
        try:
            return int(entrada)
        except ValueError:
            print("Error: Ingrese un número entero válido.")

def pedir_flotante(mensaje: str) -> float:
    while True:
        entrada = input(mensaje).strip()
        try:
            return float(entrada)
        except ValueError:
            print("Error: Ingrese un valor numérico válido.")

def menu_principal() -> None:
    print("\n" + "=" * 50)
    print("      SISTEMA RESTAURANTE - OPTIMIZADO S12       ")
    print("=" * 50)
    print("1. Registrar usuario")
    print("2. Listar usuarios")
    print("3. Registrar producto")
    print("4. Listar catálogo de productos (Stock)")
    print("5. Realizar venta de producto")
    print("6. Consultar ventas de un usuario (Índice O(1))")
    print("7. Consultar categorías únicas (Uso de set)")
    print("8. Salir")
    print("-" * 50)

def ejecutar_aplicacion() -> None:
    archivo_servicio = ArchivoServicio(ruta_base="datos")

    # Reconstrucción de estado e índices al iniciar
    restaurante = Restaurante(
        productos=archivo_servicio.cargar_productos(),
        usuarios=archivo_servicio.cargar_usuarios(),
        ventas=archivo_servicio.cargar_ventas(),
    )

    while True:
        menu_principal()
        opcion = pedir_texto("Seleccione una opción: ")

        if opcion == "1":
            print("\n--- REGISTRO DE USUARIO ---")
            identificacion = pedir_texto("Identificación: ")
            nombre = pedir_texto("Nombre: ")
            try:
                nuevo_usuario = Usuario(identificacion, nombre)
                if restaurante.agregar_usuario(nuevo_usuario):
                    archivo_servicio.guardar_usuarios(restaurante.obtener_usuarios())
                    print("Usuario registrado e indexado correctamente.")
                else:
                    print("Error: Ya existe un usuario con esa identificación.")
            except ValueError as e:
                print(f"Error de validación: {e}")

        elif opcion == "2":
            print("\n--- LISTA DE USUARIOS ---")
            usuarios = restaurante.obtener_usuarios()
            if not usuarios:
                print("No hay usuarios registrados.")
            else:
                for u in usuarios:
                    print(u)

        elif opcion == "3":
            print("\n--- REGISTRO DE PRODUCTO ---")
            codigo = pedir_texto("Código del producto: ")
            nombre = pedir_texto("Nombre del producto: ")
            categoria = pedir_texto("Categoría (ej: Platos, Bebidas, Postres): ")
            precio = pedir_flotante("Precio ($): ")
            stock = pedir_entero("Stock inicial: ")
            try:
                nuevo_producto = Producto(
                    codigo, nombre, precio, stock, categoria if categoria else "General"
                )
                if restaurante.agregar_producto(nuevo_producto):
                    archivo_servicio.guardar_productos(restaurante.obtener_productos())
                    print("Producto registrado, guardado e indexado exitosamente.")
                else:
                    print("Error: Ya existe un producto con ese código.")
            except ValueError as e:
                print(f"Error de validación: {e}")

        elif opcion == "4":
            print("\n--- CATÁLOGO DE PRODUCTOS ---")
            productos = restaurante.obtener_productos()
            if not productos:
                print("No existen productos en el inventario.")
            else:
                for p in productos:
                    print(p)

        elif opcion == "5":
            print("\n--- REGISTRAR VENTA ---")
            id_usuario = pedir_texto("Identificación del usuario: ")
            cod_producto = pedir_texto("Código del producto: ")
            cantidad = pedir_entero("Cantidad a vender: ")

            try:
                exito = restaurante.vender_producto(cod_producto, id_usuario, cantidad)
                if exito:
                    # Persistencia atómica de las colecciones afectadas
                    archivo_servicio.guardar_ventas(restaurante.obtener_ventas())
                    archivo_servicio.guardar_productos(restaurante.obtener_productos())
                    print(f"Venta procesada con éxito ({cantidad} unidad/es descontadas del inventario).")
                else:
                    print("Error en la venta: Verifique existencia de usuario/producto o stock suficiente.")
            except ValueError as e:
                print(f"Error en datos de venta: {e}")

        elif opcion == "6":
            print("\n--- CONSULTAR VENTAS POR USUARIO ---")
            id_usuario = pedir_texto("Identificación del usuario: ")
            usuario = restaurante.buscar_usuario(id_usuario)
            if usuario is None:
                print("Error: El usuario no está registrado.")
            else:
                # Comprobación de pertenencia en O(1) con set
                if not restaurante.usuario_tiene_compras(id_usuario):
                    print(f"El usuario {usuario.nombre} ({usuario.identificacion}) no tiene compras registradas.")
                else:
                    ventas_usuario = restaurante.consultar_ventas_usuario(id_usuario)
                    print(f"\nHistorial de compras de {usuario.nombre}:")
                    for idx, v in enumerate(ventas_usuario, start=1):
                        prod = restaurante.buscar_producto(v.producto_codigo)
                        nombre_prod = prod.nombre if prod else "Producto no disponible"
                        print(f"{idx}. Código: {v.producto_codigo} ({nombre_prod}) | Cantidad: {v.cantidad}")

        elif opcion == "7":
            print("\n--- CATEGORÍAS DISPONIBLES (SET) ---")
            categorias = restaurante.obtener_categorias_unicas()
            if not categorias:
                print("No hay categorías registradas en el catálogo.")
            else:
                print(f"Total de categorías únicas ({len(categorias)}):")
                for cat in sorted(categorias):
                    print(f" - {cat}")

        elif opcion == "8":
            print("\nCerrando el sistema. ¡Hasta pronto!")
            break
        else:
            print("Opción no válida. Intente nuevamente.")

if __name__ == "__main__":
    ejecutar_aplicacion()