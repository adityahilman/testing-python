from c_test import Test, SlackTest
from c_slack import SlackClient
from c_resp import jsonPayload
import os
import mysql.connector
from datetime import datetime

#print("app name :")
#app_name = input()

slack_channel = os.getenv('SLACK_CHANNEL')
app_url = "http://local.test"
incident_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
response_code = 200

# sendslack = SlackClient()
# sendslack.sendSlackDown(app_url, incident_time, slack_channel)
#print(sendslack.slack_thread_id)

# getTest = SlackTest(app_url, str(incident_time))
# #getTest.sendslack()
# print(getTest.slack_thread_id)

# sendSlack = SlackClient(app_url, str(incident_time), slack_channel, response_code)
# print(sendSlack.slack_thread_id)
jsonPost = jsonPayload(app_url, response_code, str(incident_time))
jsonPost.jsonDown()