# db/database.py

import mysql.connector
from mysql.connector import Error
from contextlib import contextmanager
import os

from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'database': os.getenv('DB_DATABASE'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD')
}

@contextmanager
def get_db_connection():
    """Gestionnaire de contexte pour la connexion à la base de données"""
    connection = None
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        yield connection
    except Error as e:
        print(f"Erreur de connexion à la base de données: {e}")
        raise
    finally:
        if connection and connection.is_connected():
            connection.close()

@contextmanager
def get_db_cursor():
    """Gestionnaire de contexte pour obtenir un curseur de base de données"""
    with get_db_connection() as connection:
        cursor = connection.cursor(dictionary=True)
        try:
            yield cursor
            connection.commit()
        except Error as e:
            connection.rollback()
            print(f"Erreur d'exécution SQL: {e}")
            raise
        finally:
            cursor.close()
