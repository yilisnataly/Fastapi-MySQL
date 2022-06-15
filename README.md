# FastAPI & MySQL

En este apartado se procede a crear una aplicación con FastAPI usando la base de datos MySQL desde un contenedor Docker, para que realice operaciones de tipo CRUD (Create, Read, Update, Delete) una vez que se establezca la conexión con la base de datos.


Para comenzar se crea un entorno virtual para instalar las librerias necesarias de Python `virtualenv`

```bash
python3.9 -m venv venv
```
Una vez creado el directorio `venv` se procede activar el entorno de la siguiente manera:

```bash
source venv/bin/activate
```
Se instalan las librerias necesarias referenciadas en el fichero requirements.txt
```bash
pip3 install -r requirements.txt
```

La aplicación esta estructura por los siguientes modulos:
```bash
.
└── api_mysql_app
    ├── __init__.py
    ├──app.py
    ├──config
    |  └──db.py
    ├──models 
    |  └──student.py
    ├──routes
    |  └──student.py
    ├──schemas
       └──student.py
 ```

El módulo `api_flask_mysql/config/db.py` configura la URL y los parametros de conexión con la base de datos. 
```bash
from sqlalchemy import create_engine, MetaData
import os


MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_ROOT_PASSWORD = os.getenv("MYSQL_ROOT_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")

URL_CONNECTION = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_ROOT_PASSWORD}@{MYSQL_HOST}:3306/{MYSQL_DATABASE}"

meta = MetaData()

engine = create_engine(URL_CONNECTION)
conn = engine.connect()
```

El módulo `api_flask_mysql/models/student.py` define los modelos de datos, atributos y columnas para la creación de la tabla de la base de datos.
```bash
from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String
from config.db import meta, engine

students = Table("students", meta, Column(
    "id", Integer, primary_key=True), 
    Column("name", String(255)), 
    Column("email", String(255)), 
    Column("phone", String(255)), 
    Column("address", String(255)))

meta.create_all(engine) #estableciendo conexion con la db para la creacion de la table
```
El módulo `api_flask_mysql/schemas/student.py` define el tipo de datos que la db estará devolviendo.
```bash
from typing import Optional
from pydantic import BaseModel


class Student(BaseModel):
    id: Optional[int]
    name: str
    email: str
    phone: str
    address: str
```

El módulo `api_flask_mysql/app.py` establece la conexión con FastAPI. 

El módulo `api_flask_mysql/routes/student.py` especifica las rutas y/o endpoints de la aplicación.
```bash
from fastapi import APIRouter, Response, status
from config.db import conn
from models.student import students
from schemas.student import Student
from starlette.status import HTTP_204_NO_CONTENT


student = APIRouter()


@student.get("/students", response_model=list[Student], tags=["students"])
def get_students():
    return conn.execute(students.select()).fetchall()  # consulta sql


@student.post("/addStudents", response_model=Student, tags=["students"])
def create_student(student: Student):
    new_student = {"name": student.name, "email": student.email,
                   "phone": student.phone, "address": student.address}
    result = conn.execute(students.insert().values(new_student))
    print(result.lastrowid)
    return conn.execute(students.select().where(students.c.id == result.lastrowid)).first()


@student.get("/students/{id}", response_model=Student, tags=["students"])
def get_student(id: str):
    return conn.execute(students.select().where(students.c.id == id)).first()


@student.delete("/students/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["students"])
def delete_student(id: str):
    result = conn.execute(students.delete().where(students.c.id == id))
    return Response(status_code=HTTP_204_NO_CONTENT)


@student.put("/students/{id}", response_model=Student, tags=["students"])
def update_student(id: str, student: Student):
    conn.execute(students.update().values(name=student.name, 
    email=student.email, phone=student.phone, address=student.address).where(students.c.id == id))
    return conn.execute(students.select().where(students.c.id == id)).first()
```

Una vez definido los módulos de la aplicación FastAPI, se procede a desplegar la base de datos con docker, por lo que se debe tener instalado `docker` y `docker-compose`, como descrito en el fichero `flask-mysql-app`. Ante todo se debe configurar las variables de entorno para establecer la conexión con la base de datos en un fichero .env, en donde se define los parametros de conexión como:
- MYSQL_USER
- MYSQL_ROOT_PASSWORD
- MYSQL_HOST
- MYSQL_DATABASE

```bash
docker compose --env-file .env.file up
```

Y luego se prueba desde el navegador los siguientes endpoints, accediendo a las siguientes URL para la creación de la tabla, e insertar los estudiantes:

1. http://localhost:5000/create-table
2. http://localhost:5000/add-students
3. http://localhost:5000/

Tras la creación de la base de datos y la tabla, se corre la aplicación FastAPI con el siguiente comando:

```bash
uvicorn app:app --reload
```
![fastapi app](https://user-images.githubusercontent.com/39458920/172646772-006fe1e2-ce90-4c1e-8419-ff1009752a8f.JPG)

Y se accede a la URL `http://127.0.0.1:8000/students` y se comprueba que muestra los datos de los estudiantes inicialmente agregados.
![fastapi_students](https://user-images.githubusercontent.com/39458920/172647803-3ffd8e23-361a-4b6d-90dd-9e3239d25785.JPG)

Para visualizar la lista de las rutas definidas, se accede a la siguiente URL `http://127.0.0.1:8000/docs`
![fastapi_portal](https://user-images.githubusercontent.com/39458920/172648981-456f8123-6491-45a0-9521-b21e26f52fb4.JPG)

Se prueba los diferentes endpoints creados:
- `GET/students` nos muestra la lista de estudiantes inicialmente creados. 

![student_list](https://user-images.githubusercontent.com/39458920/172657047-6b996b4f-a066-4c83-b1de-98d3ff09055e.JPG)

- `POST/addStudents` crea un nuevo estudiante y lo agrega a la lista.

![add_students](https://user-images.githubusercontent.com/39458920/172657203-cea36398-1b67-4873-a7ec-f98aa2e4bc3c.JPG)

- `GET/students/{id}` devuelve un único estudiante, escribiendo el número del `id`

![unico_id_test](https://user-images.githubusercontent.com/39458920/172659437-9068e05d-4564-4a34-b309-5cb1cb380582.JPG)

- `DELETE/students/{id}` elimina un estudiante especifico. Se comprueba que el estudiante ha sido eliminado consultando la lista de estudiantes `http://127.0.0.1:8000/students`

- `UPDATE/students/{id}` actualiza un usuario ya creado, ingresando solo el correspondiente `id` y los nuevos datos que queremos darle al nuevo estudiante. Se comprueba que el nuevo usuario ha sido cambiado `http://127.0.0.1:8000/students/2`
