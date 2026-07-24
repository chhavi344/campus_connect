import mysql.connector

from config import DB_HOST
from config import DB_USER
from config import DB_PASSWORD
from config import DB_NAME

# DATABASE CONNECTION 

def get_connection():

    connection = mysql.connector.connect(

        host=DB_HOST,

        user=DB_USER,

        password=DB_PASSWORD,

        database=DB_NAME

    )

    return connection