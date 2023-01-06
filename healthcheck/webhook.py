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
db_name = os.getenv("DB_NAME")
slack_channel = os.getenv('SLACK_CHANNEL')

db = mysql.connector.connect(
	host=db_host,
	user=db_user,
	passwd=db_pass,
	database=db_name
)
cursor = db.cursor(dictionary=True)

app = Flask(__name__)

@app.route("/", methods = ['GET'])
def getHome():
	response = {
		"Status": "OK"
	}
	return json.dumps(response)

@app.route("/3", methods = ['GET'])
def getH3():
	response = {
		"Status": "OK"
	}
	return json.dumps(response)

@app.route("/4", methods = ['GET'])
def getH4():
	response = {
		"Status": "OK"
	}
	return json.dumps(response)

@app.route("/5", methods = ['GET'])
def getH5():
	response = {
		"Status": "OK"
	}
	return json.dumps(response)	


@app.route('/healthcheck-webhook', methods=['POST'])
def mainRoute():
	startDowntime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	insertSql = "insert into monitoring (application_name, slack_thread_id, alert_state, start_downtime, end_downtime) values (%s, %s, %s, %s, 0)"
	responseUrl = request.json
	
	#print("json payload "+responseUrl)

	applicationName = responseUrl['incident']['resource']['labels']['host']
	responseCode = responseUrl['incident']['resource']['labels']['response_code']
	#print("app name :"+applicationName)

	alertState = responseUrl['incident']['state']
	
	responseJson = {
		"Application name": applicationName,
		"Alert State": alertState
	}

	if alertState == "open":
		slackBlockMessageDown = [
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": ":redalert: Service Down :redalert: "
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*Application Url Healtcheck :* \n"+applicationName+"\n\n*Response Code:* \n"+responseCode
			}
		},
		{
			"type": "divider"
		}
		]
		sendSlackNotif = slackClient.chat_postMessage(
			channel=slack_channel,
			text="Service Down: "+applicationName,
			blocks=slackBlockMessageDown
		)
		slackThread = sendSlackNotif['message']['ts']

		insertValue = (applicationName, slackThread, alertState, startDowntime)
		cursor.execute(insertSql, insertValue)
		db.commit()

	else:
		# get application state from database
		fetchSql = "select slack_thread_id from monitoring where alert_state='open' and application_name = %s"
		cursor.execute(fetchSql, (applicationName,))
		allResult = cursor.fetchall()
		for result in allResult:
			result["slack_thread_id"]
		
		getSlackThreadId = result['slack_thread_id']
		
		slackBlockMessageUP = [
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "Service returned to Normal state :thumbsup: "
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*Application Url Healtcheck :* \n"+applicationName+"\n\n*Response Code:* \n"+responseCode
			}
		},
		{
			"type": "divider"
		}
		]

		sendSlackReply = slackClient.chat_update(
			channel=slack_channel,
			ts=getSlackThreadId,
			text="Service returned to Normal state: "+applicationName,
			blocks=slackBlockMessageUP
		)

		# update database when service back to normal
		endDowntime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		updateSQL = """update monitoring set alert_state = 'closed', end_downtime = %s where slack_thread_id = %s """
		cursor.execute(updateSQL, (endDowntime,getSlackThreadId))
		db.commit()


	return json.dumps(responseJson)

	
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000, debug=True)