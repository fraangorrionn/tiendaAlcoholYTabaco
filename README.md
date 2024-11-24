#tiendaAlcoholYTabaco

Esta aplicación es una tienda especializada en la venta de productos de alcohol y tabaco. Permite a los usuarios realizar compras en línea, agregar productos a su lista de favoritos, y realizar reclamos si surge algún problema con los pedidos. Los usuarios pueden asociar una tarjeta de pago a su cuenta para realizar transacciones. La tienda también cuenta con un sistema de gestión de inventarios y categorías para organizar los productos disponibles.
Modelos
1. Usuario

Descripción: Representa a un usuario en el sistema.

    Atributos:
        nombre (CharField): Nombre del usuario, máximo 100 caracteres.
        correo (EmailField): Correo electrónico del usuario, único, con un valor por defecto.
        direccion (CharField): Dirección del usuario, con un valor por defecto.
        tipo_usuario (CharField): Tipo de usuario (cliente o administrador), usando choices para restringir valores.
        telefono (CharField): Número de teléfono del usuario, opcional.

2. Producto

Descripción: Representa un producto disponible en el sistema.

    Atributos:
        nombre (CharField): Nombre del producto, máximo 100 caracteres.
        precio (DecimalField): Precio del producto, con hasta 10 dígitos en total y 2 decimales.
        tipo (CharField): Tipo de producto (vino, cerveza, tabaco) con choices para restringir valores, y un valor por defecto.
        stock (IntegerField): Cantidad disponible de producto en stock.
        descripcion (TextField): Descripción del producto, opcional.
        tiempo_estimado_envio (TimeField): Tiempo estimado para el envío del producto, opcional.

3. Orden

Descripción: Representa una orden realizada por un usuario.

    Atributos:
        fecha_orden (DateField): Fecha en que se realizó la orden, se añade automáticamente.
        total (DecimalField): Total de la orden.
        estado (CharField): Estado de la orden (completada, pendiente, cancelada), restringido con choices.
        usuario (ForeignKey): Relación con el modelo Usuario, eliminando la orden si se elimina el usuario.
        metodo_pago (CharField): Método de pago utilizado, opcional.

4. DetalleOrden

Descripción: Representa los productos incluidos en una orden.

    Atributos:
        orden (ForeignKey): Relación con el modelo Orden.
        producto (ForeignKey): Relación con el modelo Producto.
        cantidad (IntegerField): Cantidad del producto en la orden, con un valor por defecto de 1.
        precio_unitario (DecimalField): Precio por unidad del producto.
        descuento_aplicado (DecimalField): Descuento aplicado a la orden, por defecto 0.
        tasa_impuesto (FloatField): Tasa de impuesto aplicada al producto.

5. Provedor

Descripción: Representa a un proveedor de productos.

    Atributos:
        nombre (CharField): Nombre del proveedor, máximo 100 caracteres.
        contacto (CharField): Nombre de contacto del proveedor, máximo 100 caracteres.
        telefono (CharField): Número de teléfono del proveedor.
        correo (EmailField): Correo electrónico del proveedor, opcional.
        activo (BooleanField): Indica si el proveedor está activo o no, con valor por defecto True.

6. Inventario

Descripción: Representa el inventario de productos.

    Atributos:
        producto (OneToOneField): Relación con el modelo Producto.
        cantidad_disponible (PositiveIntegerField): Cantidad disponible del producto.
        ubicacion (CharField): Ubicación del producto en el inventario.
        minimo_requerido (IntegerField): Cantidad mínima requerida en inventario.
        fecha_actualizacion (DateField): Fecha de la última actualización, se añade automáticamente.

7. Tarjeta

Descripción: Representa una tarjeta de pago asociada a un usuario.

    Atributos:
        usuario (OneToOneField): Relación con el modelo Usuario.
        numero_tarjeta (CharField): Número de tarjeta, máximo 16 caracteres.
        fecha_expiracion (DateField): Fecha de expiración de la tarjeta.
        tipo (CharField): Tipo de tarjeta (crédito, débito, etc.), por defecto crédito.
        codigo_seguridad (CharField): Código de seguridad de la tarjeta, opcional.

8. Favoritos

Descripción: Representa productos que un usuario ha marcado como favoritos.

    Atributos:
        usuario (ForeignKey): Relación con el modelo Usuario.
        producto (ForeignKey): Relación con el modelo Producto.
        fecha_agregado (DateField): Fecha en que se agregó a favoritos, se añade automáticamente.
        prioridad (IntegerField): Prioridad del producto en la lista de favoritos, por defecto 1.
        notas (TextField): Notas adicionales, opcional.

9. Reclamo

Descripción: Representa un reclamo realizado por un usuario.

    Atributos:
        usuario (OneToOneField): Relación con el modelo Usuario.
        detalle_orden (OneToOneField): Relación con el modelo DetalleOrden, opcional.
        descripcion (TextField): Descripción del reclamo.
        fecha (DateField): Fecha en que se realizó el reclamo, se añade automáticamente.
        estado (CharField): Estado del reclamo (pendiente, resuelto, etc.), con valor por defecto pendiente.
        respuesta (TextField): Respuesta al reclamo, opcional.

10. Categoria

Descripción: Representa una categoría de productos.

    Atributos:
        nombre (CharField): Nombre de la categoría, único, máximo 100 caracteres.
        descripcion (TextField): Descripción de la categoría, opcional.
        fecha_creacion (DateField): Fecha de creación de la categoría, se añade automáticamente.
        estado (CharField): Estado de la categoría (activo, inactivo), con valor por defecto activo.
        prioridad (IntegerField): Prioridad de la categoría, por defecto 1.

11. ProductoCategoria

Descripción: Representa la asociación entre productos y categorías.

    Atributos:
        producto (ForeignKey): Relación con el modelo Producto.
        categoria (ForeignKey): Relación con el modelo Categoria.
        fecha_asociacion (DateField): Fecha en que se asoció el producto con la categoría, se añade automáticamente.
        nota_adicional (TextField): Nota adicional sobre la asociación, opcional.
        estado (CharField): Estado de la asociación (activo, inactivo), por defecto activo.

Relaciones entre los Modelos

    Uno a Uno (1:1):
        Usuario ↔ Tarjeta
        Usuario ↔ Reclamo
        Producto ↔ Inventario
    Uno a Muchos (1
    ):
        Usuario ↔ Orden
        Usuario ↔ Favoritos
        Producto ↔ DetalleOrden
        Orden ↔ DetalleOrden
        Categoria ↔ ProductoCategoria
    Muchos a Muchos (N
    ):
        Producto ↔ Categoria (a través de ProductoCategoria)
        Usuario ↔ Producto (a través de Favoritos)
        Provedor ↔ Producto

#Vistas

1. index

Descripción: Vista principal que redirige al índice de URLs.
Requisitos cumplidos: Cumple con la funcionalidad básica de redirección.

2. lista_usuarios

Descripción: Muestra una lista de todos los usuarios registrados en la plataforma con su tarjeta y productos favoritos.
Requisitos cumplidos: Muestra datos de relaciones OneToMany y optimización mediante select_related y prefetch_related.

3. lista_productos

Descripción: Muestra una lista de todos los productos con sus categorías, ordenados por precio.
Requisitos cumplidos: Usa QuerySets y muestra datos de relaciones ManyToMany.

4. lista_ordenes

Descripción: Lista todas las órdenes con el usuario asociado, mostrando las últimas 10 órdenes.
Requisitos cumplidos: Utiliza order_by y limita la cantidad de resultados.

5. lista_detalles_orden

Descripción: Lista todos los detalles de las órdenes, incluyendo el subtotal para cada producto.
Requisitos cumplidos: Optimiza las consultas y calcula subtotales a partir de las relaciones.

6. lista_proveedores

Descripción: Lista todos los proveedores y los productos que suministran.
Requisitos cumplidos: Utiliza prefetch_related para optimizar la consulta.

7. lista_inventarios

Descripción: Muestra el inventario de productos ordenado por cantidad disponible, mostrando productos con inventario bajo el mínimo.
Requisitos cumplidos: Utiliza filter con condiciones específicas.

8. lista_tarjetas

Descripción: Lista todas las tarjetas asociadas a los usuarios, mostrando solo las tarjetas con fecha de expiración futura.
Requisitos cumplidos: Relación OneToOne y filtrado de datos.

9. lista_favoritos

Descripción: Muestra los productos favoritos de cada usuario, solo los favoritos de alta prioridad.
Requisitos cumplidos: Utiliza relaciones ManyToMany y optimiza la consulta.

10. lista_reclamos

Descripción: Lista los reclamos realizados, con opción de filtrar solo los pendientes.
Requisitos cumplidos: Usa filtros con condiciones AND/OR y optimiza la consulta.

11. lista_categorias

Descripción: Muestra las categorías activas, ordenadas por prioridad.
Requisitos cumplidos: Utiliza order_by para ordenar resultados.

12. lista_producto_categoria

Descripción: Muestra la relación entre productos y categorías, filtrando categorías activas.
Requisitos cumplidos: Utiliza relaciones ManyToMany.

13. productos_precio_mayor

Descripción: Muestra productos con precio mayor al valor especificado.
Requisitos cumplidos: Incluye un parámetro entero en la URL.

14. usuarios_con_productos_favoritos

Descripción: Lista usuarios que tienen múltiples productos favoritos en diferentes categorías.
Requisitos cumplidos: Usa annotate y filtros avanzados.

15. inventario_bajo_minimo

Descripción: Muestra productos cuyo inventario está por debajo del mínimo requerido.
Requisitos cumplidos: Usa filtro con condiciones específicas.

16. ordenes_con_total_aggregado

Descripción: Muestra la suma total de todas las órdenes.
Requisitos cumplidos: Utiliza aggregate.

17. productos_por_categoria_y_precio

Descripción: Muestra productos de una categoría específica y con precio menor a max_precio.
Requisitos cumplidos: Incluye dos parámetros en la URL.

18. ordenes_recientes

Descripción: Muestra las últimas 5 órdenes ordenadas por fecha.
Requisitos cumplidos: Usa order_by y limita los resultados.

19. usuarios_sin_telefono

Descripción: Muestra usuarios que no tienen teléfono registrado (campo None).
Requisitos cumplidos: Utiliza filtro con isnull.

20. detalle_orden_usuario

Descripción: Muestra las órdenes de un usuario específico, incluyendo detalles de cada orden.
Requisitos cumplidos: Utiliza relaciones OneToMany y prefetch_related.

21. categorias_ordenadas_por_prioridad

Descripción: Muestra categorías ordenadas por prioridad de mayor a menor.
Requisitos cumplidos: Usa order_by.

22. detalle_producto

Descripción: Muestra detalles de un producto específico por ID.
Requisitos cumplidos: Usa get_object_or_404 para la validación.

23. buscar_producto

Descripción: Busca productos por nombre.
Requisitos cumplidos: Utiliza un parámetro de tipo string.

24. buscar_productos_por_nombre_o_tipo

Descripción: Busca productos por nombre o tipo.
Requisitos cumplidos: Utiliza filtros con condiciones OR.

----------------- Templates -------------------

#Usar al menos 5 templates tags diferentes: if-else, for..empty
**Ubicación:** `templates/Paginas/detalles_orden_list.html`

**Template tags usados:**
1. `{% extends %}`: Hereda de `principal.html`.
2. `{% load %}`: Carga archivos estáticos para la plantilla.
3. `{% block ... %}`: Define bloques de contenido específicos para CSS y el cuerpo principal.
4. `{% for ... empty %}`: Itera sobre los detalles de las órdenes y muestra un mensaje si no hay resultados.
5. `{% include %}`: Incluye un template parcial para renderizar cada detalle.

### Template: operadores usados

**Ubicación:** `templates/Paginas/resultados_busqueda.html`

**Operadores usados:**
1. **`if` (Evaluación de igualdad):** Usado en `{% if productos %}` para comprobar si hay productos disponibles.
2. **`else` (Lógica alternativa):** Usado para mostrar un mensaje cuando no hay productos disponibles.
3. **`|length` (Longitud):** Usado para mostrar la cantidad de productos encontrados.
4. **`|default` (Valor predeterminado):** Usado para mostrar un texto cuando no hay consulta en la variable `query`.
5. **`for...empty` (Inclusión lógica):** Usado para iterar sobre los productos o mostrar un mensaje si no hay elementos en la lista.

### Templates filters usados
1. floatformat
**Ubicacion** `templates/Listas/productos.html`

{{ producto.precio|floatformat:2 }}
Muestra el precio con dos decimales, asegurando un formato adecuado para monedas.

2. time
**Ubicacion** `templates/Listas/detalle_producto.html`
{{ producto.tiempo_estimado_envio|time:"H:i" }}
Formatea el campo producto.tiempo_estimado_envio para mostrar solo la hora y minutos en formato HH:mm.

3. capfirst
**Ubicacion** `templates/Listas/categorias_prioridad.html`
{{ categoria.estado|capfirst }}
Convierte la primera letra del valor de categoria.estado en mayúscula, manteniendo el resto en minúsculas.
Resultado: "activo" → "Activo".

4. date
**Ubicación**  `templates/Listas/categorias.html`
{{ categoria.fecha_creacion|date:"d/m/Y" }}
Formatea el campo fecha_creacion en formato de fecha día/mes/año.

5. join
**Ubicación** `templates/Listas/usuarios_con_productos_favoritos.html`
{{ producto.categorias.all|join:", " }}
Combina todos los elementos de categorias.all en una sola cadena, separándolos con comas.
Resultado: Una lista de categorías como ["Bebidas", "Vinos", "Tintos"] se mostrará como "Bebidas, Vinos, Tintos".

6. capfirst
**Ubicación** `templates/Listas/usuarios_sin_telefono.html`
{{ usuario.tipo_usuario|capfirst }}
Convierte la primera letra del valor de tipo_usuario en mayúscula, dejando el resto en minúsculas.
Resultado: "administrador" → "Administrador".

7. slice
**Ubicación** `templates/Listas/usuarios.html`
usuario.productos_favoritos.all|slice:":5"
Limita la lista de productos favoritos a los primeros 5 elementos.
Ejemplo de resultado:
Lista completa: ["Producto1", "Producto2", "Producto3", "Producto4", "Producto5", "Producto6"]
Con slice:":5": ["Producto1", "Producto2", "Producto3", "Producto4", "Producto5"]

8. length (combinado con if)
**Ubicación** `templates/Listas/usuarios.html`
{% if usuario.productos_favoritos.all|length > 5 %}
Evalúa si hay más de 5 productos en la lista, mostrando un mensaje adicional si es el caso.

9. default
**Ubicación** `templates/Listas/ordenes.html`
{{ orden.metodo_pago|default:"No especificado" }}
Muestra el texto "No especificado" si orden.metodo_pago no tiene un valor asignado (es None o vacío).

10. add
**Ubicación** `templates/Listas/por_nombre_o_tipo.html`
{{ producto.precio|add:10|floatformat:2 }}
Suma 10 unidades al precio del producto, simulando un cálculo de impuestos u otro ajuste.
Ejemplo de resultado:
Si el precio es 100.00, el resultado será 110.00.