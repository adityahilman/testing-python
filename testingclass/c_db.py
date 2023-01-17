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
        self.insertAppStatus()


    def getAppList(self):
        getAppList = "select * from app_list where application_health_status = 1"
        DatabaseClient.cursor.execute(getAppList)
        allResult = DatabaseClient.cursor.fetchall()
        return allResult
        # for appList in allResult:
        #     print("List application : ",dict(appList))

    

    #def insertAppStatus(self, app_url, slack_thread_id, alert_state, incident_time: str, recovered_time: str=None):
    def insertAppStatus(self):
        #print("from class db: ",self.app_url, self.slack_thread_id, self.alert_state, self.incident_time)
        insertAppStatus = "insert into app_healthcheck (application_url, slack_thread_id, alert_state, incident_at, recovered_at) values (%s, %s, %s, %s, 0)"
        DatabaseClient.cursor.execute(insertAppStatus, (self.app_url,self.slack_thread_id, self.alert_state, self.incident_time))
        DatabaseClient.connect.commit()

    
    def updateAppStatus(self, app_url):
        self.app_url = app_url
        print("app dari database client: ",self.app_url)
        updateAppStatus = "update app_list set application_health_status = 0 where application_url = %s"
        DatabaseClient.cursor.execute(updateAppStatus, (self.app_url,))
        DatabaseClient.connect.commit()
        #print("Database updated")