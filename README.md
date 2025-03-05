# Permisos de Acceso en la API

## Permisos para **Gerentes**

### Reclamo
- **Can add reclamo** → Puede **crear** reclamos  
- **Can change reclamo** → Puede **editar** reclamos  
- **Can delete reclamo** → Puede **eliminar** reclamos  
- **Can view reclamo** → Puede **ver** reclamos  

### Tarjeta
- **Can add tarjeta** → Puede **crear** tarjetas  
- **Can change tarjeta** → Puede **editar** tarjetas  
- **Can delete tarjeta** → Puede **eliminar** tarjetas  
- **Can view tarjeta** → Puede **ver** tarjetas  

### Usuario
- **Can add user** → Puede **crear** usuarios  
- **Can change user** → Puede **editar** usuarios  
- **Can delete user** → Puede **eliminar** usuarios  
- **Can view user** → Puede **ver** usuarios  

### Proveedor
- **Can add provedor** → Puede **crear** proveedores  
- **Can change provedor** → Puede **editar** proveedores  
- **Can delete provedor** → Puede **eliminar** proveedores  
- **Can view provedor** → Puede **ver** proveedores  

### Producto
- **Can add producto** → Puede **crear** productos  
- **Can change producto** → Puede **editar** productos  
- **Can delete producto** → Puede **eliminar** productos  
- **Can view producto** → Puede **ver** productos  

### Inventario
- **Can add inventario** → Puede **crear** inventarios  
- **Can change inventario** → Puede **editar** inventarios  
- **Can delete inventario** → Puede **eliminar** inventarios  
- **Can view inventario** → Puede **ver** inventarios  

### Orden
- **Can add orden** → Puede **crear** órdenes  
- **Can change orden** → Puede **editar** órdenes  
- **Can delete orden** → Puede **eliminar** órdenes  
- **Can view orden** → Puede **ver** órdenes  

### Categoría
- **Can add categoria** → Puede **crear** categorías  
- **Can change categoria** → Puede **editar** categorías  
- **Can delete categoria** → Puede **eliminar** categorías  
- **Can view categoria** → Puede **ver** categorías  

### Detalle de Orden
- **Can add detalle orden** → Puede **crear** detalles de orden  
- **Can change detalle orden** → Puede **editar** detalles de orden  
- **Can delete detalle orden** → Puede **eliminar** detalles de orden  
- **Can view detalle orden** → Puede **ver** detalles de orden  

### Favoritos
- **Can add favoritos** → Puede **crear** favoritos  
- **Can change favoritos** → Puede **editar** favoritos  
- **Can delete favoritos** → Puede **eliminar** favoritos  
- **Can view favoritos** → Puede **ver** favoritos  

### Entrada de Registro (Log Entry)
- **Can view log entry** → Puede **ver** entradas de registro  
- **Can add log entry** → Puede **crear** entradas de registro  
- **Can change log entry** → Puede **editar** entradas de registro  
- **Can delete log entry** → Puede **eliminar** entradas de registro  

---

## Permisos para **Usuarios**

### Reclamo
- **Can add reclamo** → Puede **crear** reclamos  
- **Can view reclamo** → Puede **ver** reclamos  

### Tarjeta
- **Can view tarjeta** → Puede **ver** tarjetas  

### Usuario
- **Can view user** → Puede **ver** usuarios  

### Proveedor
- **Can view provedor** → Puede **ver** proveedores  

### Producto
- **Can view producto** → Puede **ver** productos  

### Inventario
- **Can view inventario** → Puede **ver** inventarios  

### Orden
- **Can view orden** → Puede **ver** órdenes  

### Categoría
- **Can view categoria** → Puede **ver** categorías  

### Detalle de Orden
- **Can view detalle orden** → Puede **ver** detalles de orden  

### Favoritos
- **Can add favoritos** → Puede **crear** favoritos  
- **Can view favoritos** → Puede **ver** favoritos  

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