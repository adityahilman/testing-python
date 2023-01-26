import mysql.connector
import os
from mysql.connector import Error

class DatabaseClient:

    def __init__(self, app_url=None, slack_thread_id=None, alert_state=None, incident_time=None, recovered_time=None ):
        self.app_url = app_url
        self.slack_thread_id = slack_thread_id
        self.alert_state = alert_state
        self.incident_time = incident_time
        self.recovered_time = recovered_time
        self.cursor = None
        self.connector = None
        try:
            self.on_connect()
        except Error as err:
            print("Database Error :", err)

   
    def on_connect(self):
        db_host = os.getenv('DB_HOST')
        db_user = os.getenv('DB_USER')
        db_pass = os.getenv('DB_PASS')
        db_name = os.getenv("DB_NAME")

        self.connector = mysql.connector.connect(
            host=db_host, 
            user=db_user,
            passwd=db_pass,
            database=db_name,
            autocommit=True
            )
        self.cursor = self.connector.cursor(dictionary=True)
        


    def getAllAppList(self):
        getAllAppList = "select * from app_list"
        self.cursor.execute(getAllAppList)
        result_app_list = self.cursor.fetchall()
        return result_app_list
    