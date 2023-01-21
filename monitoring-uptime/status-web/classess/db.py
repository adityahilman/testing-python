import mysql.connector
import os

class DatabaseClient:
    db_host = os.getenv('DB_HOST')
    db_user = os.getenv('DB_USER')
    db_pass = os.getenv('DB_PASS')
    db_name = os.getenv("DB_NAME")
    
    connect = mysql.connector.connect(
        host=db_host,
        user=db_user,
        passwd=db_pass,
        database=db_name, 
        autocommit=True
    )

    cursor = connect.cursor(dictionary=True)

    def __init__(self, app_url=None, slack_thread_id=None, alert_state=None, incident_time=None, recovered_time=None ):
        self.app_url = app_url
        self.slack_thread_id = slack_thread_id
        self.alert_state = alert_state
        self.incident_time = incident_time
        self.recovered_time = recovered_time

    def getAllAppList(self):
        getAllAppList = "select * from app_list"
        DatabaseClient.cursor.execute(getAllAppList)
        result_app_list = DatabaseClient.cursor.fetchall()
        return result_app_list
    