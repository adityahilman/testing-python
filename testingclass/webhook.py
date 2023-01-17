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

@app.route('/healthcheck-webhook', methods=['POST'])
def healthcheckWebhook():
    jsonPost = request.json
    incident_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    app_url = jsonPost['incident']['resource']['labels']['host']
    response_code = jsonPost['incident']['resource']['labels']['response_code']
    alert_state = jsonPost['incident']['state'] 
    #print(slack_channel)

    if alert_state == "open":
        sendSlackNotif = SlackClient(app_url, str(incident_time), slack_channel, response_code)
        sendSlackNotif.sendSlackDown()
        
        # insert incident to database
        insert_to_db = DatabaseClient()
        insert_to_db.insertAppStatus(app_url,sendSlackNotif.slack_thread_id, alert_state, incident_time)
    
    else:
        get_slack_thread_id = DatabaseClient()
        get_slack_thread_id.getSlackThreadId(app_url)
        all_result = DatabaseClient.cursor.fetchall()
        for result in all_result:
            result["slack_thread_id"]

        slack_thread_id = result["slack_thread_id"]
        recovered_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        update_to_db = DatabaseClient()
        update_to_db.updateAppStatus(app_url, slack_thread_id, str(recovered_time))
        # if alert_state == "closed"
        sendSlackNotif = SlackClient(app_url, incident_time, slack_channel, slack_thread_id, str(recovered_time))
        sendSlackNotif.sendSlackUp()
        print("closed")
    return json.dumps(jsonPost)


   

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=9000, debug=True)