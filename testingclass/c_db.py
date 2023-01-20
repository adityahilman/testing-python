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


    def getAppList(self):
        getAppList = "select * from app_list where application_health_status = 1"
        DatabaseClient.cursor.execute(getAppList)
        allResult = DatabaseClient.cursor.fetchall()
        return allResult

    def getAppStatusDown(self):
        sqlGetAppStatusDown = "select * from app_list where application_health_status = 0"
        DatabaseClient.cursor.execute(sqlGetAppStatusDown)
        allResult = DatabaseClient.cursor.fetchall()
        return allResult


    def getSlackThreadId(self, app_url):
        self.app_url = app_url
        sqlGetSlackThreadId = "select slack_thread_id, incident_at from app_healthcheck where alert_state='open' and application_url = %s"
        DatabaseClient.cursor.execute(sqlGetSlackThreadId, (self.app_url,))
        result_slack_thread_id = DatabaseClient.cursor.fetchall()
        return result_slack_thread_id
    

    def insertAppStatus(self, app_url, slack_thread_id, alert_state, incident_time: str, recovered_time: str=None):
    #def insertAppStatus(self):
        self.app_url = app_url
        self.slack_thread_id = slack_thread_id
        self.alert_state = alert_state
        self.incident_time = incident_time
        self.recovered_time = recovered_time
        print("from class db: ",self.app_url, self.slack_thread_id, self.alert_state, self.incident_time)
        insertAppStatus = "insert into app_healthcheck (application_url, slack_thread_id, alert_state, incident_at, recovered_at) values (%s, %s, %s, %s, 0)"
        DatabaseClient.cursor.execute(insertAppStatus, (self.app_url,self.slack_thread_id, self.alert_state, self.incident_time))
        DatabaseClient.connect.commit()

    
    def updateAppStatus(self, app_url:str, application_health_status:int):
        self.app_url = app_url
        self.application_health_status = application_health_status
        print("app dari database client: ",self.app_url, self.application_health_status)
        sqlUpdateAppStatus = "update app_list set application_health_status = %s where application_url = %s"
        DatabaseClient.cursor.execute(sqlUpdateAppStatus, (self.application_health_status, self.app_url))
        DatabaseClient.connect.commit()
        #print("Database updated")
    
    def updateAppAlertState(self, app_url, slack_thread_id, recovered_time:str):
        self.app_url = app_url
        self.slack_thread_id = slack_thread_id
        self.recovered_time = recovered_time
        updateAppAlertState = "update app_healthcheck set alert_state='closed', recovered_at = %s where slack_thread_id = %s"
        DatabaseClient.cursor.execute(updateAppAlertState, (self.recovered_time, self.slack_thread_id))
        DatabaseClient.connect.commit()
        return("dari update alert state : ",self.app_url, self.slack_thread_id, self.recovered_time)
