# tiendaAlcoholYTabaco

# Modelos

1. Usuario

    Descripción: Representa a un usuario en el sistema.
    Atributos:
        nombre: (CharField) Nombre del usuario, máximo 100 caracteres.
        correo: (EmailField) Correo electrónico único del usuario, con un valor por defecto.
        direccion: (CharField) Dirección del usuario, con un valor por defecto.
        tipo_usuario: (CharField) Tipo de usuario (cliente o administrador).
        telefono: (CharField) Número de teléfono del usuario, opcional.

2. Producto

    Descripción: Representa un producto disponible en el sistema.
    Atributos:
        nombre: (CharField) Nombre del producto, máximo 100 caracteres.
        precio: (DecimalField) Precio del producto, con hasta 10 dígitos en total y 2 decimales.
        tipo: (CharField) Tipo de producto (vino, cerveza, tabaco) con un valor por defecto.
        stock: (IntegerField) Cantidad de producto disponible en stock.
        descripcion: (TextField) Descripción del producto, opcional.

3. Orden

    Descripción: Representa una orden realizada por un usuario.
    Atributos:
        fecha_orden: (DateField) Fecha en que se realizó la orden, se añade automáticamente.
        total: (DecimalField) Total de la orden.
        estado: (CharField) Estado de la orden (completada, pendiente, cancelada).
        usuario: (ForeignKey) Relación con el modelo Usuario, eliminando la orden si se elimina el usuario.
        metodo_pago: (CharField) Método de pago utilizado, opcional.

4. DetalleOrden

    Descripción: Representa los productos incluidos en una orden.
    Atributos:
        orden: (ForeignKey) Relación con el modelo Orden.
        producto: (ForeignKey) Relación con el modelo Producto.
        cantidad: (IntegerField) Cantidad del producto en la orden, por defecto 1.
        precio_unitario: (DecimalField) Precio por unidad del producto.
        descuento_aplicado: (DecimalField) Descuento aplicado a la orden, por defecto 0.

5. Provedor

    Descripción: Representa a un proveedor de productos.
    Atributos:
        nombre: (CharField) Nombre del proveedor, máximo 100 caracteres.
        contacto: (CharField) Nombre de contacto del proveedor, máximo 100 caracteres.
        telefono: (CharField) Número de teléfono del proveedor.
        correo: (EmailField) Correo electrónico del proveedor, opcional.

6. Inventario

    Descripción: Representa el inventario de productos.
    Atributos:
        producto: (OneToOneField) Relación con el modelo Producto.
        cantidad_disponible: (IntegerField) Cantidad disponible del producto.
        ubicacion: (CharField) Ubicación del producto en el inventario.
        minimo_requerido: (IntegerField) Cantidad mínima requerida en inventario.
        fecha_actualizacion: (DateField) Fecha de la última actualización, se añade automáticamente.

7. Tarjeta

    Descripción: Representa una tarjeta de pago asociada a un usuario.
    Atributos:
        usuario: (OneToOneField) Relación con el modelo Usuario.
        numero_tarjeta: (CharField) Número de tarjeta, máximo 16 caracteres.
        fecha_expiracion: (DateField) Fecha de expiración de la tarjeta.
        tipo: (CharField) Tipo de tarjeta (crédito, débito, etc.), por defecto crédito.
        codigo_seguridad: (CharField) Código de seguridad de la tarjeta, opcional.

8. Favoritos

    Descripción: Representa productos que un usuario ha marcado como favoritos.
    Atributos:
        usuario: (ForeignKey) Relación con el modelo Usuario.
        producto: (ForeignKey) Relación con el modelo Producto.
        fecha_agregado: (DateField) Fecha en que se agregó a favoritos, se añade automáticamente.
        prioridad: (IntegerField) Prioridad del producto en la lista de favoritos, por defecto 1.
        notas: (TextField) Notas adicionales, opcional.

9. Reclamo

    Descripción: Representa un reclamo realizado por un usuario.
    Atributos:
        usuario: (OneToOneField) Relación con el modelo Usuario.
        descripcion: (TextField) Descripción del reclamo.
        fecha: (DateField) Fecha en que se realizó el reclamo, se añade automáticamente.
        estado: (CharField) Estado del reclamo (pendiente, resuelto, etc.), por defecto pendiente.
        respuesta: (TextField) Respuesta al reclamo, opcional.

10. Categoria

    Descripción: Representa una categoría de productos.
    Atributos:
        nombre: (CharField) Nombre de la categoría, único, máximo 100 caracteres.
        descripcion: (TextField) Descripción de la categoría, opcional.
        fecha_creacion: (DateField) Fecha de creación de la categoría, se añade automáticamente.
        estado: (CharField) Estado de la categoría (activo, inactivo), por defecto activo.
        prioridad: (IntegerField) Prioridad de la categoría, por defecto 1.

11. ProductoCategoria

    Descripción: Representa la asociación entre productos y categorías.
    Atributos:
        producto: (ForeignKey) Relación con el modelo Producto.
        categoria: (ForeignKey) Relación con el modelo Categoria.
        fecha_asociacion: (DateField) Fecha en que se asoció el producto con la categoría, se añade automáticamente.
        nota_adicional: (TextField) Nota adicional sobre la asociación, opcional.
        estado: (CharField) Estado de la asociación (activo, inactivo), por defecto activo.

# Relaciones entre los Modelos

1. Usuario

    Relación con Orden: Un usuario puede realizar múltiples órdenes, lo que se representa como una relación uno a muchos (1:M). Un registro en la tabla Usuario puede estar vinculado a varios registros en la tabla Orden.

    Relación con Tarjeta: Un usuario puede tener solo una tarjeta asociada (1:1), representada por un OneToOneField. Esto significa que cada usuario tiene como máximo una tarjeta de pago.

    Relación con Favoritos: Un usuario puede tener múltiples productos en su lista de favoritos (1
    ). Un registro en Usuario puede estar vinculado a varios registros en Favoritos.

    Relación con Reclamo: Un usuario puede hacer un reclamo. La relación es uno a uno (1:1), lo que significa que un usuario puede tener un reclamo asociado.

2. Producto

    Relación con DetalleOrden: Un producto puede aparecer en múltiples detalles de órdenes, y cada detalle de orden se refiere a un producto específico. Esto es una relación uno a muchos (1: M).

    Relación con Inventario: Un producto puede tener solo un registro de inventario asociado (1:1). Esto permite una relación directa entre la disponibilidad del producto y sus datos en el inventario.

    Relación con Favoritos: Un producto puede ser agregado a la lista de favoritos de múltiples usuarios (1
    ). Esto significa que un producto puede estar en la lista de favoritos de varios usuarios.

    Relación con ProductoCategoria: Un producto puede estar asociado a múltiples categorías a través de la tabla intermedia ProductoCategoria, estableciendo una relación muchos a muchos (M:M).

3. Orden

    Relación con DetalleOrden: Una orden puede contener múltiples detalles, donde cada detalle se refiere a un producto específico. Esto es una relación uno a muchos (1
    ).

    Relación con Usuario: Como se mencionó anteriormente, cada orden está asociada a un solo usuario, lo que es una relación uno a muchos (1
    ).

4. DetalleOrden

    Relación con Orden: Cada detalle de orden está vinculado a una única orden (1
    ).

    Relación con Producto: Cada detalle de orden se refiere a un solo producto, pero un producto puede aparecer en múltiples detalles de orden (1
    ).

5. Provedor

    Relación con Producto: Aunque no está especificada en el modelo, típicamente un proveedor puede ofrecer múltiples productos (1
    ), lo que permitiría asociar productos con sus respectivos proveedores.

6. Inventario

    Relación con Producto: Cada producto tiene un solo registro de inventario asociado (1:1). Esto permite controlar la cantidad y ubicación de cada producto en el inventario.

7. Tarjeta

    Relación con Usuario: Cada tarjeta está asociada a un único usuario (1:1). Un usuario puede tener solo una tarjeta.

8. Favoritos

    Relación con Usuario: Cada favorito está vinculado a un único usuario (N:1).

    Relación con Producto: Cada favorito está asociado a un único producto (N:1). Esto permite que un producto pueda estar en la lista de favoritos de varios usuarios.

9. Reclamo

    Relación con Usuario: Cada reclamo está vinculado a un único usuario (1:1). Esto significa que cada usuario puede tener un reclamo específico.

10. Categoria

    Relación con ProductoCategoria: Cada categoría puede estar asociada a múltiples productos a través de la tabla ProductoCategoria, estableciendo una relación uno a muchos (1:N).

11. ProductoCategoria

    Relación con Producto: Cada asociación en ProductoCategoria se refiere a un solo producto (N:1).

    Relación con Categoria: Cada asociación en ProductoCategoria se refiere a una sola categoría (N:1). Esto permite que un producto pueda estar en varias categorías y viceversa.

Resumen de Relaciones

    Uno a Uno (1:1): Usuario ↔ Tarjeta, Usuario ↔ Reclamo, Producto ↔ Inventario.
    Uno a Muchos (1:N): Usuario ↔ Orden, Usuario ↔ Favoritos, Producto ↔ DetalleOrden, Orden ↔ DetalleOrden, Categoria ↔ ProductoCategoria.
    Muchos a Muchos (N: N): Producto ↔ Categoria a través de ProductoCategoria.