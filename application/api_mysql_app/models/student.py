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