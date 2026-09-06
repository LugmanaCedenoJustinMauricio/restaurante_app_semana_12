# Sistema de Gestión de Restaurante - restaurante_app (Semana 12)

**Asignatura:** Programación Orientada a Objetos  
**Institución:** Universidad Estatal Amazónica (UEA)  
**Estudiante:** Justin Mauricio Lugmaña Cedeño  
**Tema:** colecciones orientados al rendimiento

---

## 1. Descripción del Sistema
La versión de la **Semana 12** de `restaurante_app` mantiene todas las funcionalidades de inventario, stock, clientes, ventas y persistencia JSON trabajadas previamente, incorporando una **refactorización interna de rendimiento** mediante estructuras de datos complementarias en memoria (`dict` y `set`).

El objetivo es eliminar los recorridos secuenciales repetitivos de orden O(n) en operaciones frecuentes de búsqueda, agrupación y validación, logrando accesos directos de tiempo constante promedio O(1) sin romper el encapsulamiento ni alterar la interfaz pública consumida por la capa de presentación.

---

## 2. Estructura Modular del Proyecto

```text
restaurante_app/
├── datos/
│   ├── productos.json
│   ├── usuarios.json
│   └── ventas.json
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   ├── usuario.py
│   └── venta.py
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py
│   └── restaurante.py
├── main.py
└── README.md
```

### Responsabilidad de los Componentes
* **`modelos/`**: Conserva las entidades del dominio (`Producto`, `Usuario`, `Venta`) con sus validaciones y encapsulamiento estricto.
* **`servicios/archivo_servicio.py`**: Administra la persistencia atómica en JSON, gestionando rutas y excepciones de archivos (`FileNotFoundError`, `JSONDecodeError`, `PermissionError`).
* **`servicios/restaurante.py`**: Centraliza la lógica de negocio, mantiene las listas principales para persistencia y administra la sincronización y reconstrucción de los **índices en memoria**.
* **`main.py`**: Punto de entrada e interfaz de consola que interactúa con los servicios sin manipular colecciones directamente.

---
## 3. Mejoras de Rendimiento y Colecciones Utilizadas

* **Búsqueda de producto por código:** Se sustituyó el recorrido secuencial en `list` (O(n)) por el diccionario `_productos_por_codigo: dict[str, Producto]`, logrando acceso directo en tiempo constante **O(1)**.
* **Búsqueda de usuario por identificación:** Se sustituyó la iteración lineal (O(n)) por el diccionario indexado `_usuarios_por_identificacion: dict[str, Usuario]`, reduciendo la consulta a **O(1)**.
* **Consulta de ventas por usuario:** En lugar de recorrer y filtrar la colección general de ventas en cada petición (O(n)), se indexaron en el diccionario agrupado `_ventas_por_usuario: dict[str, list[Venta]]` para retorno inmediato **O(1)**.
* **Verificación de compras de usuario:** Se implementó el conjunto `_usuarios_con_compras: set[str]` para validar pertenencia en **O(1)** mediante el operador `in` sin recorrer listas.
* **Gestión de categorías únicas:** Se utilizó el conjunto `_categorias: set[str]` para asegurar unicidad automática y validación instantánea de categorías existentes.

### Criterios de Sincronización y Reconstrucción

1. **Reconstrucción inicial:** Al iniciar el aplicativo, el método privado `_reconstruir_indices()` recorre las listas cargadas desde JSON una única vez para poblar los diccionarios y conjuntos en memoria.
2. **Sincronización en caliente:** Al registrar un producto, usuario o procesar una venta, la aplicación actualiza simultáneamente la lista principal y los índices correspondientes.
3. **Persistencia limpia:** Los índices no se guardan en el disco; se regeneran dinámicamente en el arranque del sistema a partir de los archivos JSON.

## 4. Instrucciones de Clonación y Ejecución

### 1. Clonar el repositorio
```bash
git clone 
```

### 2. Ingresar al directorio del proyecto
```bash
cd restaurante_app_semana_12/restaurante_app
```
*(o ingresar secuencialmente: `cd restaurante_app_semana_12` y luego `cd restaurante_app`)*

### 3. Ejecutar la aplicación
* **En Windows (lanzador rápido):**
```bash
py main.py
```
* **En Windows / Linux / macOS (estándar):**
```bash
python main.py
```
* **En Linux / macOS (especificando Python 3):**
```bash
python3 main.py
```

---

## 5. Pruebas Realizadas y Comprobación de Funcionamiento
1. **Reconstrucción de Índices:** Se inició el sistema con datos preexistentes en `datos/` y se verificó que las búsquedas por código e ID respondieron de forma inmediata sin recorrer listas completas.
2. **Búsqueda Directa:** Se consultaron productos y usuarios existentes y no existentes mediante `buscar_producto()` y `buscar_usuario()`, confirmando respuestas en tiempo constante O(1) vía `.get()`.
3. **Venta y Sincronización:** Se ejecutó una venta válida; el stock se descontó correctamente, el objeto `Venta` se agregó a la lista principal, a `_ventas_por_usuario` y su ID se indexó en `_usuarios_con_compras`.
4. **Consulta Filtrada:** La opción 6 devolvió las ventas del cliente directamente desde el índice agrupado sin iterar por ventas ajenas.
5. **Categorías Únicas:** La opción 7 comprobó pertenencia y unicidad mediante el conjunto `set`, mostrando las categorías sin valores repetidos.
6. **Reinicio y Persistencia:** Se cerró el programa y se volvió a abrir, confirmando que JSON recuperó el inventario actualizado y los índices se reconstruyeron en memoria de manera íntegra.