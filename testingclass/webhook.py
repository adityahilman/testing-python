from flask import Flask, request
import json
import requests
from datetime import datetime
from c_slack import SlackClient
import os

slack_channel = os.getenv('SLACK_CHANNEL')

app = Flask(__name__)

@app.route('/healthcheck-webhook', methods=['POST'])
def healthcheckWebhook():
    jsonPost = request.json
    incidentTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    app_url = jsonPost['incident']['resource']['labels']['host']
    response_code = jsonPost['incident']['resource']['labels']['response_code']
    alert_state = jsonPost['incident']['state']

    if alert_state == "open":
        sendSlackNotif = SlackClient(slack_channel, app_url, 0)
        sendSlackNotif.sendSlackDown()

   

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=9000, debug=True)