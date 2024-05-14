from peewee import *
import pymysql

class DatabaseConfig:
    db = MySQLDatabase(
        'db_iot_activity', 
        user='iot_activity_user', 
        password='t4Hf^yOd', 
        host='websocket.rezurrection.website', 
        port=3306
    )
    
    @staticmethod
    def initialize():
        DatabaseConfig.db.connect()
        # DatabaseConfig.db.create_tables([Activity, Room, Participant], safe=True)
        DatabaseConfig.db.close()

class BaseModel(Model):
    """Classe de base pour tous les modèles, utilisant la même connexion à la base de données."""
    class Meta:
        database = DatabaseConfig.db

    @classmethod
    def get_all(cls):
        return cls.select()