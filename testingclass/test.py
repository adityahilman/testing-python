from datetime import datetime
from c_test import Test
from c_slack import SlackClient
from c_db import DatabaseClient
import os

slack_channel = os.getenv('SLACK_CHANNEL')

app_url = "http://local.com"
incident_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
response_code = 200
slack_thread_id = "123123123"
alert_state = "open"

# sendSlackNotif = SlackClient(app_url, str(incident_time), slack_channel, response_code)
# sendSlackNotif.sendSlackDown()
# print("slack thread id :",sendSlackNotif.slack_thread_id)

getTest = DatabaseClient()
getTest.insertAppStatus(app_url, slack_thread_id, alert_state, str(incident_time) )