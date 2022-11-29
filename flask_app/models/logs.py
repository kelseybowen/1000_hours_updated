from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_app.models import users
from flask import flash
from flask_bcrypt import Bcrypt
import datetime
import re

class Log:
    db = "1000_hours_schema"
    def __init__(self, data):
        self.id = data["id"]
        self.date = data["date"]
        self.minutes = data["minutes"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]
        self.formatted_date = Log.convert_date(self.date)
        
    @classmethod
    def get_all_user_logs(cls, data):
        query = "SELECT * FROM logs WHERE user_id = %(user_id)s;"
        data = {
            "user_id": data
        }
        results = connectToMySQL(cls.db).query_db(query, data)
        logs = []
        for log in results:
            logs.append(cls(log))
        return logs
    
    @classmethod
    def get_one_log(cls, data):
        query = "SELECT * FROM logs WHERE id = %(id)s;"
        data = {
            "id": data
        }
        result = connectToMySQL(cls.db).query_db(query, data)
        return cls(result[0])
    
    @classmethod
    def create_log(cls, data):
        query = "INSERT INTO logs (date, minutes, created_at, updated_at, user_id) VALUES (%(date)s, %(minutes)s, NOW(), NOW(), %(user_id)s);"
        data = {
            "date": data["date"],
            "minutes": data["minutes"],
            "user_id": data
        }
        result = connectToMySQL(cls.db).query_db(query, data)
        return result
    
    @staticmethod
    def convert_date(date):
        date_data = datetime.datetime(date.year, date.month, date.day)
        conv_date = date_data.strftime("%B %d, %Y")
        return conv_date