# Taller

## Serializers

¿Qué son en si los serializadores?, dentro de DRF (Django Rest Framework) los serializadores son nuestros transformadores de datos de Python a JSON. Por ejemplo, de nuestro modelo TODO, tenemos los siguientes datos.

```py
class Todo(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    done_at = models.DateField(null=True)
    updated_at = models.DateField(auto_now_add=True)
    deleted_at = models.DateField(null=True)
    status = models.IntegerField(default=0)
```

Pero dentro de nuestra vista de la API, los datos son mostrados de la siguiente forma:

```json
[
    {
        "id": 1,
        "title": "Todo1",
        "body": "Primer todo de Ejemplo",
        "created_at": "2022-12-07",
        "done_at": null,
        "updated_at": "2022-12-07",
        "deleted_at": null,
        "status": 0
    },
    {
        "id": 2,
        "title": "Todo 2",
        "body": "Todo creado desde RapidApi",
        "created_at": "2022-12-07",
        "done_at": null,
        "updated_at": "2022-12-07",
        "deleted_at": null,
        "status": 0
    },
    {
        "id": 3,
        "title": "Todo1",
        "body": "Primer todo de Ejemplo",
        "created_at": "2022-12-07",
        "done_at": null,
        "updated_at": "2022-12-07",
        "deleted_at": null,
        "status": 0
    }
]
```

Esto es gracias al serializer que hemos creado, mediante el es que se envía la información al serializer el cual realiza la conversión entre nuestros datos nativos de la base de datos, al formato de JSON que debe ser enviado al frontend o viceversa.

```py
from rest_framework import serializers
from .models import Todo

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = (
            "id",
            "title",
            "body",
            "created_at",
            "done_at",
            "updated_at",
            "deleted_at",
            "status",
        )
        read_only_fields = 'created_at', 'done_at', 'updated_at', 'deleted_at'
```

¿Y si queremos hacer operaciones CRUD?

En otras versiones de DRF, es necesario crear otros tipos de vistas para poder extraer un solo elemento o hacer un listing de los mismos. Pero únicamente con nuestro router creado en estas últimas versiones, contamos con el soporte necesario para hacer estas operaciones sin necesidad de añadir código. Posteriormente crearemos este tipo de vista para operaciones más específicas, pero por ahora usaremos lo base para interactuar con nuestro serializador.

### Recordando operaciones del CRUD

Dentro del crud, tenemos 4 distintos tipos de acciones.

-   CREATE
    
    -   Permite la creación de nuevos registros, también conocido como POST.
-   RETRIEVE
    
    -   Sirve para obtener los datos de nuestro servidor, podemos obtenerlos en conjunto o cada registro individual.
-   UPDATE
    
    -   Permite la actualización de un registro, en este tipo de acción contamos con dos formas de actualización.
        
        -   PUT: Realiza la actualización de todo el registro.
            
        -   PATCH: Realiza la actualización de un único campo del registro.
            
-   DELETE
    
    -   Sirve para eliminar un registro o varios.

Todas estas operaciones están totalmente soportadas por nuestro serializer.

-   CREATE:

![CREATE](https://photos.silabuz.com/uploads/big/7c5c9bb20f9011b051d9cad08aeec120.PNG)

-   RETRIEVE

![RETRIEVE](https://photos.silabuz.com/uploads/big/f9f6c8e00bea9adf76581ce07748e817.PNG)

-   UPDATE
    
    -   PUT
        
        ![PUT](https://photos.silabuz.com/uploads/big/19031feb963984cc2a8406e336b6bc0b.PNG)
        
    -   PATCH
        
        ![PATCH](https://photos.silabuz.com/uploads/big/7b1ddab154aabd0704e5637aad672a80.PNG)
        
-   DELETE
    

![DELETE](https://photos.silabuz.com/uploads/big/de51ebdce0c4a74c30597f233b2abc98.PNG)

## Serializers no basados en modelos

Sin basarnos es la estructura de un modelo, podemos definir nuestro propios serializador para poder apreciar de mejor forma como es su funcionamiento. Por ejemplo, para cada campo de un modelo dentro del serializador existe un tipo de dato (char, boolean, etc).

Para crear nuestro propio serializador, realizamos lo siguiente dentro de `todos/serializers.py`:

```py
class TestTodoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length = 100)
    body = serializers.CharField()
```

Como se puede apreciar, este ya no está definido por un modelo, si no que nosotros mismo estamos definiendo los campos y los tipos de datos que contiene.

¿Cómo lo probamos?

Para probarlo modificaremos nuestro `TodoViewSet` de `api.py`:

```py
from .serializers import TestTodoSerializer

class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = TestTodoSerializer
```

Si ejecutamos nuestro servidos, y accedemos a la ruta para obtener los datos, vemos la siguiente información:

![Serializer propio](https://photos.silabuz.com/uploads/big/4e0fefaa96155374ec6927c66adefad4.PNG)

¡Únicamente aparecen los campos que hemos definido!

Por lo que ahora podemos agregar nuevas funciones al momento de utilizar métodos como GET, POST, etc.

> No podemos agregar campos que no pertenezcan al modelo que haga referencia.

### Personalizando validaciones

Dentro de nuestro propio serializer, podemos hacer validaciones propias.

```py
class TestTodoSerializer(serializers.Serializer):
    title = serializers.CharField(max_length = 100)
    body = serializers.CharField()

    def validate_title(self, value):
        # Validación customizada
        if "$" in value:
            raise serializers.ValidationError("Error, el título no puede tener el símbolo de $")
        return value
    
    def validate_body(self, value):
        # Validación customizada
        if "$" in value:
            raise serializers.ValidationError("Error, el cuerpo no puede tener el símbolo de $")
        return value
```

> Para que sea tomado como una validación de un campo, la función debe tener la siguiente estructura: `validate_<field_name>`

Ahora que tenemos una validación para que no se pueda agregar "$" dentro de la creación de un TODO, si probamos ingresarlo, obtenemos la siguiente respuesta.

![Validación customizada](https://photos.silabuz.com/uploads/big/be730cd96987731aa967d39c086292ab.PNG)

Con esto ya tenemos la posibilidad de crear nuestra propias validaciones.

## Cors

Con Django Rest Framework crearemos una Rest Api, lo que significa que vamos a consumirlo desde una aplicación exterior que podría estar desarrollado con React por ejemplo. Para poder consumir nuestra Rest Api sin problemas tenemos que configurar estos permisos.

Para eso instalaremos `django-cors-headers`:

```
pip install django-cors-headers
```

Luego lo añadiremos en aplicaciones instaladas dentro de `settings.py`:

```python
INSTALLED_APPS = [
    ...,
    'corsheaders',
    ...,
]
```

También necesitamos agregar middlewares:

```python
MIDDLEWARE = [
    ...,
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    ...,
]
```

Configurar el comportamiento de los middlewares para que sólo ciertas aplicaciones puedan acceder:

```python
CORS_ALLOWED_ORIGINS = [
  "
https://mywebsite.com
",
  "
https://blog.mywebsite.com
",
  "
http://localhost:8080
",
  "
http://127.0.0.1:9000
",
]
```

En este caso permitiremos cualquier aplicación, por lo que solo agregaremos:

```python
CORS_ALLOW_ALL_ORIGINS = True
```

Con todo esto, ya deberíamos tener la posibilidad de tener acceso a nuestra API desde cualquier tipo de cliente que utilicemos.

## Tarea

Realizar la conexión correcta del repositorio del frontend, con el backend sin que existe problemas con CORS.

-   [FrontEnd](https://github.com/silabuzinc/demo-cors)

Crea un serializador con todos los datos del modelo TODO y añadir todas las excepciones o errores que presenten los campos (datos nulos, texto vacío, etc.).

-   Nota: Añadir validaciones propias para su serializador.

1.  Con la conexión realizada, haga el ingreso de 30 registros TODO, directamente en la API creada para ser mostrados en el frontend.
    
2.  Realize PUT de 10 registros tanto en la vista que ofrece DRF, como en otro API cliente como Postman, RapidAPI, etc.
    
3.  Realice PATCH de 15 registros tanto en la vista que ofrece DRF, como en otro API cliente como Postman, RapidAPI, etc.
    
4.  Realice DELETE de 5 registros tanto en la vista que ofrece DRF, como en otro API cliente como Postman, RapidAPI, etc.
    

## Adicional

Investigar como validar que un campo es nulo o no. Luego, implementar la validación personalizada para un campo nulo.

Links:
- Videos
 [Teoria Part 1](https://www.youtube.com/watch?v=OCg7Wsh_kpI&list=PLxI5H7lUXWhgHbHF4bNrZdBHDtf0CbEeH&index=3&ab_channel=Silabuz)
 [Teoria Part 2](https://www.youtube.com/watch?v=9mIPn-_NjDg&list=PLxI5H7lUXWhgHbHF4bNrZdBHDtf0CbEeH&index=4&ab_channel=Silabuz)
 [Practica](https://www.youtube.com/watch?v=P8xltXI4rqI&list=PLxI5H7lUXWhgHbHF4bNrZdBHDtf0CbEeH&index=5&ab_channel=Silabuz)
- Slide
 [Slide](https://docs.google.com/presentation/d/e/2PACX-1vQlRaq25V_7tT64EZNDakLJ_FLh5njIeTwfMe9xjJ1aBHfKc0tEsJ1x9w3CuMfpYhP8xbLElfW4aznW/embed?start=false&loop=false&delayms=3000)