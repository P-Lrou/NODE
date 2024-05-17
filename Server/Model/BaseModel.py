from peewee import *
import pymysql
from tools.DLog import DLog

class DatabaseConfig:

    @staticmethod
    def get_database():
        try:
            db = MySQLDatabase(
                'db_iot_activity',
                user='iot_activity_user',
                password='t4Hf^yOd',
                host='websocket.rezurrection.website',
                port=3306
            )
            db.connect()
            return db
        except Exception as e:
            DLog.LogError(f"Error connecting to the database: {e}")
            return None

class BaseModel(Model):
    """Classe de base pour tous les modèles, utilisant la même connexion à la base de données."""
    class Meta:
        database = DatabaseConfig.get_database()

    @classmethod
    def get_all(cls):
        return cls.select()

    @classmethod
    def test_connection(cls):
        if cls._meta.database:
            try:
                cls.get_all()
                return True
            except Exception as e:
                DLog.LogError(f"Error connecting to '{cls._meta.table_name}' table: {e}")
        return False