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

# FORMULARIOS

# Widgets utilizados en los formularios del proyecto
1-forms.EmailInput:
    Usado para campos de correo electrónico, como el correo en el formulario UsuarioModelForm y ProvedorModelForm.

2-forms.Select:
    Usado para desplegables con una sola selección, como tipo de usuario, estado de la orden, y usuario asociado en los formularios UsuarioModelForm, OrdenModelForm, y ProvedorModelForm.

3-forms.NumberInput:
    Usado para entradas de números, como total de la orden, cantidad disponible y mínimo requerido en los formularios OrdenModelForm e InventarioModelForm.

4-forms.Textarea:
    Usado para campos de texto largo, como descripción en el formulario CategoriaModelForm.

5-forms.CheckboxSelectMultiple:
    Usado para desplegables con selección múltiple, como productos favoritos en los formularios UsuarioModelForm y ProvedorModelForm.

6-forms.ClearableFileInput:
   Usado para permitir la carga de archivos en el formulario, como el campo archivo_adjunto** en el formulario OrdenModelForm.

# Validaciones en Formularios

# Validaciones en el Formulario de Usuario

### **1. Validación del Nombre del Usuario:**
- **Campo:** `nombre`
- **Condición:** El nombre no debe exceder los **100 caracteres**.
- **Validación:** Si el nombre es más largo de lo permitido, se generará un error.
- **Mensaje de error:** `El nombre no debe exceder los 100 caracteres.`

### **2. Validación del Correo Electrónico:**
- **Campo:** `correo`
- **Condición:** El correo debe tener un formato válido y ser único.
- **Validación:** 
  - Se verifica que el correo electrónico tenga un formato válido (ejemplo: `usuario@example.com`).
  - Se valida que el correo no exista ya en la base de datos para evitar duplicados.
- **Mensaje de error:** 
  - `El correo electrónico no tiene un formato válido.`
  - `Ya existe un usuario con este correo electrónico.`

### **3. Validación del Teléfono:**
- **Campo:** `telefono`
- **Condición:** El teléfono debe tener entre **7 y 15 dígitos** y puede incluir un prefijo "+".
- **Validación:** Si el teléfono no cumple con el formato esperado, se genera un error.
- **Mensaje de error:** `El teléfono debe tener entre 7 y 15 dígitos y puede incluir un prefijo '+'.`


## Formulario de **Orden**

### **1. Validación de Total:**
- **Campo:** `total`
- **Condición:** El total debe ser un número mayor que **0**.
- **Validación:** Si el valor es `0` o negativo, se mostrará un mensaje de error indicando que el total debe ser mayor a 0.
- **Ejemplo de mensaje de error:** `El total debe ser mayor a 0.`

### **2. Validación de Método de Pago:**
- **Campo:** `metodo_pago`
- **Condición:** El campo no puede estar vacío o contener solo espacios en blanco.
- **Validación:** Si el campo no tiene un valor válido, se mostrará un mensaje de error.
- **Ejemplo de mensaje de error:** `Debe especificar un método de pago.`

### **3. Validación de Estado:**
- **Campo:** `estado`
- **Condición:** Si el estado es **"pendiente"**, el total no debe ser mayor a **1000**.
- **Validación:** Si se intenta guardar una orden con el estado **pendiente** y un total superior a 1000, se muestra un mensaje de error.
- **Ejemplo de mensaje de error:** `Las órdenes pendientes no pueden tener un total mayor a 1000.`

# Validaciones en el Formulario de Proveedor

### **1. Validación del Nombre del Proveedor:**
- **Campo:** `nombre`
- **Condición:** El nombre del proveedor debe ser único.
- **Validación:** Si el nombre ingresado ya existe en la base de datos, se generará un error de validación.
- **Mensaje de error:** `Ya existe un proveedor con este nombre.`

### **2. Validación del Teléfono:**
- **Campo:** `telefono`
- **Condición:** El teléfono debe tener entre 7 y 15 dígitos y puede incluir un prefijo `+`.
- **Validación:** Si el teléfono no sigue este formato, se generará un error.
- **Mensaje de error:** `El teléfono debe tener entre 7 y 15 dígitos y puede incluir un prefijo '+'.`

### **3. Validación del Correo Electrónico:**
- **Campo:** `correo`
- **Condición:** El correo electrónico debe ser único.
- **Validación:** Si el correo electrónico ya está registrado en otro proveedor, se generará un error.
- **Mensaje de error:** `Ya existe un proveedor con este correo electrónico.`

### **4. Validación de Productos Asociados:**
- **Campo:** `productos`
- **Condición:** El proveedor debe tener al menos un producto asociado.
- **Validación:** Si no se selecciona ningún producto, se generará un error.
- **Mensaje de error:** `Debe seleccionar al menos un producto.`

# Validaciones en el Formulario de Inventario

### **1. Validación de `cantidad_disponible`:**
- **Campo:** `cantidad_disponible`
- **Condición:** La cantidad disponible debe ser mayor que **0**.
- **Validación:** Si el valor es **0 o negativo**, se muestra un mensaje de error.
- **Mensaje de error:** `La cantidad disponible debe ser mayor a 0.`

### **2. Validación de `minimo_requerido`:**
- **Campo:** `minimo_requerido`
- **Condición:** El valor de `minimo_requerido` no puede ser mayor que la `cantidad_disponible`.
- **Validación:** Si el mínimo requerido es mayor que la cantidad disponible, se muestra un mensaje de error.
- **Mensaje de error:** `El mínimo requerido no puede ser mayor que la cantidad disponible.`

# Validaciones en el Formulario de Tarjeta

### **1. Validación del Número de Tarjeta:**
- **Campo:** `numero_tarjeta`
- **Condición:** El número de tarjeta debe tener exactamente **16 dígitos** y ser numérico.
- **Validación:** Si el número de tarjeta no tiene 16 dígitos o contiene caracteres no numéricos, se genera un error de validación.
- **Mensaje de error:** `El número de tarjeta debe tener exactamente 16 dígitos y solo contener números.`

### **2. Validación de la Fecha de Expiración:**
- **Campo:** `fecha_expiracion`
- **Condición:** La fecha de expiración debe ser **posterior a la fecha actual**.
- **Validación:** Si la fecha de expiración es anterior o igual a la fecha actual, se genera un error de validación.
- **Mensaje de error:** `La tarjeta ha expirado. Debe tener una fecha posterior a hoy.`

### **3. Validación del Código de Seguridad:**
- **Campo:** `codigo_seguridad`
- **Condición:** El código de seguridad debe tener **entre 3 y 4 dígitos**.
- **Validación:** Si el código tiene menos de 3 o más de 4 dígitos, o contiene caracteres no numéricos, se genera un error de validación.
- **Mensaje de error:** `El código de seguridad debe tener entre 3 y 4 dígitos.`

# Validaciones en el Formulario de Categoría

### **1. Validación del Nombre de la Categoría:**
- **Campo:** `nombre`
- **Condición:** El nombre debe ser único.
- **Validación:** Si ya existe una categoría con el mismo nombre, se generará un error.
- **Mensaje de error:** `Ya existe una categoría con este nombre.`

### **2. Validación del Estado:**
- **Campo:** `estado`
- **Condición:** El estado debe ser **'activo'** o **'inactivo'**.
- **Validación:** Si el estado no es uno de estos dos valores, se generará un error.
- **Mensaje de error:** `El estado debe ser 'activo' o 'inactivo'.`

### **3. Validación de la Prioridad:**
- **Campo:** `prioridad`
- **Condición:** La prioridad debe ser mayor que 0.
- **Validación:** Si la prioridad es 0 o menor, se generará un error.
- **Mensaje de error:** `La prioridad debe ser un número mayor que 0.`

### PUNTO EXTRA- Permitir que en tu aplicación se incluyan imagenes o archivos y que se puedan ver

Se añadió un campo FileField en el modelo orden para almacenar archivos adjuntos en la orden.
Se actualizaron las migraciones para reflejar los cambios en la base de datos.
Se modificó el formulario para permitir la carga de archivos.
Se actualizó la vista para manejar archivos cargados usando request.FILES.
Se configuraron las URLs y ajustes de MEDIA para servir los archivos subidos.

# Permisos y Sesiones


Aquí tienes el texto listo para copiar y pegar directamente en tu README.md:

Documentación de la Aplicación
1. Tipos de Usuarios
Nuestra aplicación incluye dos tipos de usuarios claramente diferenciados, además del administrador:

Cliente: Usuario que puede realizar compras, gestionar sus productos favoritos y ver sus órdenes.
Gerente: Usuario que puede gestionar inventarios, órdenes, productos y usuarios.

Estos roles se definen en el modelo Usuario mediante el campo rol y se asignan a grupos (Clientes o Gerentes) con permisos diferenciados.

2. Control de Permisos en Vistas
Cada vista controla los permisos y verifica si el usuario está logueado utilizando:

Decorador @permission_required: Restringe el acceso a usuarios sin los permisos necesarios.
Autenticación: Si el usuario no está autenticado, se redirige al login.

@permission_required('tienda.view_producto')
def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'Paginas/productos_list.html', {'productos': productos})

3. Control de Permisos en Templates
En los templates, se verifica si el usuario está logueado y se controla el acceso al contenido según su rol y permisos.

Ejemplo de control en la cabecera: {% if perms.tienda.add_categoria %}

4. Variables de Sesión
Las siguientes variables se guardan en la sesión y aparecen en la cabecera:

fecha_inicio: Fecha y hora de inicio de sesión.
nombre_usuario: Nombre del usuario logueado.
rol: Rol del usuario en formato legible.
productos_favoritos: Número de productos favoritos del usuario.

Estas variables se eliminan automáticamente al cerrar sesión:
    def logout_view(request):
        logout(request)
        request.session.flush()
        return redirect('login')

5. Registro de Usuarios con Validaciones
El formulario de registro permite crear usuarios de tipo Cliente o Gerente, con las siguientes validaciones:

Cliente: Debe proporcionar una dirección válida.
Gerente: Debe proporcionar un teléfono válido.
6. Funcionalidades de Login y Logout
La aplicación incluye un sistema de autenticación que permite a los usuarios:

Iniciar sesión con su nombre de usuario y contraseña.
Cerrar sesión, eliminando las variables de sesión.
7. Funcionalidad de Select Dinámico
El contenido de los campos ManyToMany o ManyToOne varía según el usuario logueado. Por ejemplo, en el formulario de órdenes, los usuarios de tipo Cliente solo ven sus propias órdenes.

8. Inclusión Automática del Usuario en Formularios
En los formularios de creación, el usuario logueado se incluye automáticamente. Por ejemplo, en el formulario de órdenes, el campo usuario se llena con el usuario logueado.

9. Funcionalidad de Búsqueda Filtrada
Los formularios de búsqueda incluyen filtros dinámicos según el usuario logueado. Por ejemplo, los Clientes solo ven sus propias órdenes, mientras que los Gerentes pueden ver todas.

10. Reinicio de Contraseña
Se implementó la funcionalidad de reinicio de contraseña utilizando el sistema interno de Django. En local, el enlace de recuperación se obtiene directamente desde la consola del servidor.

## Permisos para Gerentes
Tienda | reclamo | Can add reclamo
Tienda | reclamo | Can change reclamo
Tienda | reclamo | Can delete reclamo
Tienda | reclamo | Can view reclamo
Tienda | tarjeta | Can add tarjeta
Tienda | tarjeta | Can change tarjeta
Tienda | tarjeta | Can delete tarjeta
Tienda | tarjeta | Can view tarjeta
Tienda | usuario | Can add user
Tienda | usuario | Can change user
Tienda | usuario | Can delete user
Tienda | usuario | Can view user
Tienda | provedor | Can add provedor
Tienda | provedor | Can change provedor
Tienda | provedor | Can delete provedor
Tienda | provedor | Can view provedor
Tienda | producto | Can add producto
Tienda | producto | Can change producto
Tienda | producto | Can delete producto
Tienda | producto | Can view producto
Tienda | inventario | Can add inventario
Tienda | inventario | Can change inventario
Tienda | inventario | Can delete inventario
Tienda | inventario | Can view inventario
Tienda | orden | Can add orden
Tienda | orden | Can change orden
Tienda | orden | Can delete orden
Tienda | orden | Can view orden
Tienda | categoria | Can add categoria
Tienda | categoria | Can change categoria
Tienda | categoria | Can delete categoria
Tienda | categoria | Can view categoria
Tienda | detalle orden | Can add detalle orden
Tienda | detalle orden | Can change detalle orden
Tienda | detalle orden | Can delete detalle orden
Tienda | detalle orden | Can view detalle orden
Tienda | favoritos | Can add favoritos
Tienda | favoritos | Can change favoritos
Tienda | favoritos | Can delete favoritos
Tienda | favoritos | Can view favoritos
Administración | entrada de registro | Can view log entry
Administración | entrada de registro | Can add log entry
Administración | entrada de registro | Can change log entry
Administración | entrada de registro | Can delete log entry

## Permisos para Usuarios
Tienda | reclamo | Can add reclamo
Tienda | reclamo | Can view reclamo
Tienda | tarjeta | Can view tarjeta
Tienda | usuario | Can view user
Tienda | provedor | Can view provedor
Tienda | producto | Can view producto
Tienda | inventario | Can view inventario
Tienda | orden | Can view orden
Tienda | categoria | Can view categoria
Tienda | detalle orden | Can view detalle orden
Tienda | favoritos | Can add favoritos
Tienda | favoritos | Can view favoritos

# Fixtures
Utilizo python manage.py dumpdata auth.group auth.permission --indent 4 > tienda/fixtures/grupos_y_permisos.json
para crearme los grupos y permisos

python3 -m pip install django # instalar django
python3 -m pip install django-seed # instalar seed
python3 -m pip install djangorestframework # isntalar restframework

------Comando-------
python3 -m venv myvenv
source myvenv/bin/activate

python -m pip install --upgrade pip
pip install -r requirements.txt

python manage.py migrate
python manage.py makemigrations tienda
python manage.py migrate tienda
python manage.py seed tienda --number=20
python manage.py dumpdata --indent 4 > tienda/fixtures/datos.json
python manage.py loaddata tienda/fixtures/datos.json

python manage.py createsuperuser
python manage.py runserver

git add . git commit -m 'Completado' git push git pull

curl -X POST "http://0.0.0.0:8000/oauth2/token/" -d "grant_type=password&username=fran&password=2004&client_id=mi_aplicacion&client_secret=mi_clave_secreta"
M6nbn1Oji8Q2Sh8pW7GdCLYSfanE5x