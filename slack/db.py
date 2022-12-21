import mysql.connector
import os
import json
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

slack_token = os.getenv('SLACK_TOKEN')
slackClient = WebClient(token=slack_token)

db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_pass = os.getenv('DB_PASS')

db = mysql.connector.connect(
    host=db_host,
    user=db_user,
    passwd=db_pass,
    database="dbname"
)
cursor = db.cursor()

# global variable
input_app_name = input("App name: ")
#input_alert_state = input("Alert state: ")


def insertDb():
    # send notif to slack
    sendSlackNotif = slackClient.chat_postMessage(
        channel="G01E624R14Z",
        text="Cek database app name: " +input_app_name 
    )
    # get slack thread id
    slackThreadId = sendSlackNotif['message']['ts']

    # insert ke db
    insertFunction = "insert into monitoring (application_name, slack_thread_id, alert_state) values (%s, %s, %s)"
    value = (input_app_name, slackThreadId, input_alert_state)
    cursor.execute(insertFunction, value)
    db.commit()

    print("slack thread id: " +slackThreadId)
    fetchDb()

def fetchDb():

    fetchSql = "SELECT slack_thread_id FROM monitoring WHERE application_name=%s"
    fetchValue = (input_app_name)
    cursor.execute(fetchSql, fetchValue)
    fetchResult = cursor.fetchall()
    
    getSlackThreadId = json.dumps(fetchResult)
    # debug
    print("dari function fetchDB")
    print("fetch value " +fetchValue)
    #print("sql " +fetchSql)
    print(getSlackThreadId, input_app_name)


    sendSlackReply = slackClient.chat_postMessage(
        channel="xxxx",
        thread_ts=getSlackThreadId,
        text="Hore,, dapat nih thread id nya: " +getSlackThreadId+ ":verified:"
	)
    
#insertDb()
fetchDb()