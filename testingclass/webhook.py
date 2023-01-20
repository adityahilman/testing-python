from flask import Flask, request
import json
import requests
from datetime import datetime
from c_slack import SlackClient
from c_db import DatabaseClient
from c_test import Test
import os

slack_channel = os.getenv('SLACK_CHANNEL')

app = Flask(__name__)
db_client = DatabaseClient()
slack_client = SlackClient()

@app.route('/healthcheck-webhook', methods=['POST'])
def healthcheckWebhook():
    jsonPost = request.json
    incident_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    app_url = jsonPost['incident']['resource']['labels']['host']
    response_code = jsonPost['incident']['resource']['labels']['response_code']
    alert_state = jsonPost['incident']['state'] 
    #print(slack_channel)

    if alert_state == "open":
        # sendSlackNotif = SlackClient(app_url, str(incident_time), slack_channel, response_code)
        slack_client.sendSlackDown(app_url, str(incident_time), slack_channel, response_code)
        
        # insert incident to database
        db_client.insertAppStatus(app_url,slack_client.slack_thread_id, alert_state, incident_time)
    
    else:
        print("app url :",app_url)

        get_incident_time = db_client.getSlackThreadId(app_url)
        for result_incident_time in get_incident_time:
            history_incident_time = result_incident_time["incident_at"]
            slack_thread_id = result_incident_time["slack_thread_id"]
        
        # print("history incident time: ", history_incident_time)
        # print("closed slack thread id dari webhook: ",slack_thread_id)
        recovered_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # update to database
        db_client.updateAppAlertState(app_url, slack_thread_id, str(recovered_time))

        # if alert_state == "closed"
        # sendSlackNotif = SlackClient()
        slack_client.sendSlackUp(app_url, history_incident_time, slack_channel, slack_thread_id, str(recovered_time), response_code)
        # print("closed")
    return json.dumps(jsonPost)


   

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=9000, debug=True)