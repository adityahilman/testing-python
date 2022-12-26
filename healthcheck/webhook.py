from flask import Flask, render_template, request, Response
import boto3
import json
import datetime
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from botocore.exceptions import ClientError

import mysql.connector

# slack config
slack_token = os.getenv('SLACK_TOKEN')
slackClient = WebClient(token=slack_token)

# db connector
db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_pass = os.getenv('DB_PASS')
db = mysql.connector.connect(
	host=db_host,
	user=db_user,
	passwd=db_pass,
	database="dbname"
)
cursor = db.cursor(dictionary=True)

app = Flask(__name__)

@app.route('/gcp-webhook', methods=['POST'])
def mainRoute():

	insertSql = "insert into monitoring (application_name, slack_thread_id, alert_state) values (%s, %s, %s)"
	responseUrl = request.json
	applicationName = responseUrl['incident']['resource']['labels']['host']
	alertState = responseUrl['incident']['state']
	

	if alertState == "open":
		print("Service Down")
		slackBlockMessageDown = [
		{
			"type": "divider"
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": ":redalert: *Service Down*"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*Applicaton Name:*\n" + applicationName
			}
		},
		{
			"type": "divider"
		}
		]
		sendSlackNotif = slackClient.chat_postMessage(
			channel="xxx",
			text="Service Down: "+applicationName,
			blocks=slackBlockMessageDown
		)
		slackThread = sendSlackNotif['message']['ts']

		insertValue = (applicationName, slackThread, alertState)
		cursor.execute(insertSql, insertValue)
		db.commit()
		print("function 1 - cek db")

	else:
		print("Service UP")
		# fetch function
		fetchSql = "select slack_thread_id from monitoring where alert_state='open' and application_name = %s"
		cursor.execute(fetchSql, (applicationName,))
		allResult = cursor.fetchall()
		for result in allResult:
			result["slack_thread_id"]
		
		getSlackThreadId = result['slack_thread_id']
		
		print("======================================")

		print("dari function retry")
		print("slack thread id: "+getSlackThreadId)        
		
		slackBlockMessageUP = [
		{
			"type": "divider"
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*Service returned to Normal state* :verified:"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*Applicaton Name:*\n" + applicationName + " :verified:"
			}
		},
		{
			"type": "divider"
		}
		]

		sendSlackReply = slackClient.chat_update(
			channel="xxx",
			ts=getSlackThreadId,
			text="Service returned to Normal state: "+applicationName,
			blocks=slackBlockMessageUP
		)

		# update function
		print("thread id: "+getSlackThreadId)
		updateSQL = """update monitoring set alert_state = 'closed' where slack_thread_id = %s """
		cursor.execute(updateSQL, (getSlackThreadId,))

		# updateSQL = """update monitoring set alert_state = "closed" where slack_thread_id = "1672039865.453219" """		
		# cursor.execute(updateSQL)
		db.commit()

	responseJson = {
		"Application name": applicationName
	}
	return json.dumps(responseJson)
	# return applicationName

	
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000, debug=True)