# APIRouter permite definir subrutas o rutas por separado
from fastapi import APIRouter, Response, status
from config.db import conn
from models.student import students
from schemas.student import Student
from starlette.status import HTTP_204_NO_CONTENT
from hypercorn.asyncio import serve
from hypercorn.config import Config as HyperCornConfig
from prometheus_client import Counter

student = APIRouter()

REQUESTS = Counter('server_requests_total', 'Total number of requests to this webserver')
HEALTHCHECK_REQUESTS = Counter('healthcheck_requests_total', 'Total number of requests to healthcheck')
MAIN_ENDPOINT_REQUESTS = Counter('main_requests_total', 'Total number of requests to main endpoint')
GET_LIST_ENDPOINT_REQUESTS = Counter('get_list_requests_total', 'Total number of requests to get list endpoint')
CREATE_ENDPOINT_REQUESTS = Counter('create_requests_total', 'Total number of requests to create endpoint')
GET_STUDENT_ENDPOINT_REQUESTS = Counter('get_student_requests_total', 'Total number of requests to get student endpoint')
DELETE_STUDENT_ENDPOINT_REQUESTS = Counter('delete_student_requests_total', 'Total number of requests to delete student endpoint')
UPDATE_STUDENT_ENDPOINT_REQUESTS = Counter('update_student_requests_total', 'Total number of requests to update student endpoint')


class SimpleServer:
   """
   SimpleServer class define FastAPI configuration and implemented endpoints
   """

   _hypercorn_config = None

   def __init__(self):
       self._hypercorn_config = HyperCornConfig()

    #First execution
   async def run_server(self):
       """Starts the server with the config parameters"""
       #We run server in 8081 port with 90s of timeout
       self._hypercorn_config.bind = ['0.0.0.0:8081']
       self._hypercorn_config.keep_alive_timeout = 90
       await serve(student, self._hypercorn_config)

   @student.get("/health")
   async def health_check():
        """Implement health check endpoint"""
        #Increment counter used for register the total number of calls in the webserver
        REQUESTS.inc()
        #Increment counter used for register the requests to healtcheck endpoint
        HEALTHCHECK_REQUESTS.inc()
        return {"health": "ok"}

   @student.get("/")
   async def read_main():
        """Implement main endpoint"""
        #Increment counter used for register the total number of calls in the webserver
        REQUESTS.inc()
        #Increment counter used for register the total number of calls in the main endpoint
        MAIN_ENDPOINT_REQUESTS.inc()
        return {"msg": "Hello World"}

   @student.get("/students", response_model=list[Student], tags=["students"])
   async def get_students():
        return conn.execute(students.select()).fetchall()  # consulta sql
        
        """Implement get list endpoint"""
        #Increment counter used for register the total number of calls in the webserver
        REQUESTS.inc()
        #Increment counter used for register the requests to bye endpoint
        GET_LIST_ENDPOINT_REQUESTS.inc()
        return {"msg": "Student list displayed"}


   @student.post("/addStudents", response_model=Student, tags=["students"])
   async def create_student(student: Student):
        new_student = {"name": student.name, "email": student.email, #creamos una nueva variable llamada new_student, que va a crear una nueva propiedad name y va
        #va estar basada en student.name
                   "phone": student.phone, "address": student.address}
        result = conn.execute(students.insert().values(new_student)) #llamamos el objeto conexion para realizar una consulta que la hacemos desde la tabla students
        # e insertamos un nuevo dato con el .values desde la variable new students
        print(result.lastrowid)# muestra el ultimo id agregado
        return conn.execute(students.select().where(students.c.id == result.lastrowid)).first() # nos devuelve el student que acaba de hacer creado
        
        """Implement create endpoint"""
        # Increment counter used for register the total number of calls in the webserver
        REQUESTS.inc()
        # Increment counter used for register the requests to bye endpoint
        CREATE_ENDPOINT_REQUESTS.inc()
        return {"msg": "New student added"}

   @student.get("/students/{id}", response_model=Student, tags=["students"])
   async def get_student(id: str):
        return conn.execute(students.select().where(students.c.id == id)).first()
        """Implement create endpoint"""
        # Increment counter used for register the total number of calls in the webserver
        REQUESTS.inc()
        # Increment counter used for register the requests to bye endpoint
        GET_STUDENT_ENDPOINT_REQUESTS.inc()
        return {"msg": "show new student id"}


   @student.delete("/students/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["students"])
   async def delete_student(id: str):
        result = conn.execute(students.delete().where(students.c.id == id))
        return Response(status_code=HTTP_204_NO_CONTENT)
        """Implement create endpoint"""
        # Increment counter used for register the total number of calls in the webserver
        REQUESTS.inc()
        # Increment counter used for register the requests to bye endpoint
        DELETE_STUDENT_ENDPOINT_REQUESTS.inc()
        return {"msg": "student removed"}


   @student.put("/students/{id}", response_model=Student, tags=["students"])
   async def update_student(id: str, student: Student):
        conn.execute(students.update().values(name=student.name, 
        email=student.email, phone=student.phone, address=student.address).where(students.c.id == id))
        return conn.execute(students.select().where(students.c.id == id)).first()
        """Implement create endpoint"""
        # Increment counter used for register the total number of calls in the webserver
        REQUESTS.inc()
        # Increment counter used for register the requests to bye endpoint
        UPDATE_STUDENT_ENDPOINT_REQUESTS.inc()
        return {"msg": "student updated"}
