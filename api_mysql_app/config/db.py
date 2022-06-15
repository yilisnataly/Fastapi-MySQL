from sqlalchemy import create_engine, MetaData
import os


USER_DATABASE = os.getenv("USER_DATABASE")
PASSWORD_DATABASE = os.getenv("PASSWORD_DATABASE")
HOST_DATABASE = os.getenv("HOST_DATABASE")
NAME_DATABASE = os.getenv("NAME_DATABASE")

URL_CONNECTION = f"mysql+pymysql://{USER_DATABASE}:{PASSWORD_DATABASE}@{HOST_DATABASE}:3306/{NAME_DATABASE}"

meta = MetaData() # se define meta para saber mas propiedades dentro de la tabla

engine = create_engine(URL_CONNECTION)
conn = engine.connect()

