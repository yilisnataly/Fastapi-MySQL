from fastapi import FastAPI
from routes.student import student
import asyncio

from prometheus_client import start_http_server
from routes.student import SimpleServer

app = FastAPI(
    title="Keepcoding Masters API",
    description="Our first API using python and mysql",
    version="0.0.1",
    openapi_tags=[{
            "name": "students",
            "description":"students routes"
    }]
)

app.include_router(student) #especificando las rutas que vienen del modulo student

class Container:
    """
    Class Container configure necessary methods for launch application
    """

    def __init__(self):
        self._simple_server = SimpleServer()

    async def start_server(self):
        """Function for start server"""
        await self._simple_server.run_server()


if __name__ == "__main__":
    start_http_server(8000)
    container = Container()
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(container.start_server(), loop=loop)
    loop.run_forever()