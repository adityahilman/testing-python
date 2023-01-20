from datetime import datetime
from c_test import Test
from c_slack import SlackClient
from c_db import DatabaseClient
import os

slack_channel = os.getenv('SLACK_CHANNEL')

app_url = "http://localhost:8000/5"
incident_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
response_code = 200
slack_thread_id = "123123123"
alert_state = "open"

recovered_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# sendSlackNotif = SlackClient(app_url, str(incident_time), slack_channel, response_code)
# sendSlackNotif.sendSlackDown()
# print("slack thread id :",sendSlackNotif.slack_thread_id)

# getTest = DatabaseClient()
# #getTest.updateAppAlertState(app_url, slack_thread_id, str(recovered_time) )
# resultSlackThreadId = getTest.getSlackThreadId(app_url)
# for result_slack_thread_id in resultSlackThreadId:
#     print(result_slack_thread_id['slack_thread_id'])


get_database = DatabaseClient()
get_database.updateAppStatus(app_url, "0")