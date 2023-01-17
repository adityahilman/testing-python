import mysql.connector
import os

class DatabaseConnector:
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

class DatabaseSelect:

    def getSlackThreadId(self):
        pass

    def getAppList(self):
        getAppList = "select * from app_list where application_health_status = 1"
        DatabaseConnector.cursor.execute(getAppList)
        allResult = DatabaseConnector.cursor.fetchall()
        return allResult
        # for appList in allResult:
        #     print("List application : ",dict(appList))

        
class DatabaseUpdate:

    def __init__(self, slack_thread, alert_state, incident_time, app_url):
        self.app_url = app_url
        self.slack_thread = slack_thread
        self.alert_state = alert_state
        self.incident_time = incident_time


    def insertAppStatus(self):
        insertAppStatus = "insert into app_healthcheck (application_name, slack_thread_id, alert_state, incident_at, recovered_at) values (%s, %s, %s, %s, 0)"
        DatabaseConnector.cursor.execute(insertAppStatus, )

    
    def updateAppStatus(self):
        
        updateAppStatus = "update app_list set application_health_status = 0 where application_url = %s"
        DatabaseConnector.cursor.execute(updateAppStatus, (self.app_url,))
        DatabaseConnector.connect.commit()
        print("Database updated")