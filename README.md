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