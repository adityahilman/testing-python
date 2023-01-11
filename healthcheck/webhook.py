from flask import Flask, render_template, request, Response
import json
from datetime import datetime
import os
from slack_sdk import WebClient
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

@app.route("/2", methods = ['GET'])
def getH2():
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
	startDowntime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	insertSql = "insert into app_healthcheck (application_name, slack_thread_id, alert_state, down_at, up_at) values (%s, %s, %s, %s, 0)"
	responseUrl = request.json
	
	applicationName = responseUrl['incident']['resource']['labels']['host']
	responseCode = responseUrl['incident']['resource']['labels']['response_code']
	alertState = responseUrl['incident']['state']
	
	responseJson = {
		"Application name": applicationName,
		"Alert State": alertState
	}

	if alertState == "open":
		# send slack message
		slackBlockMessageDown = [
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": ":redalert: Service Down :redalert: "
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*Application Url Healtcheck :* \n"+applicationName+ \
					"\n\n*Response Code:* \n"+responseCode+ \
					"\n\n*Downtime at:* \n"+startDowntime
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
		fetchSql = "select slack_thread_id from app_healthcheck where alert_state='open' and application_name = %s"
		cursor.execute(fetchSql, (applicationName,))
		allResult = cursor.fetchall()
		for result in allResult:
			result["slack_thread_id"]
		
		getSlackThreadId = result['slack_thread_id']
		endDowntime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

		# update database when service back to normal
		updateSQL = """update app_healthcheck set alert_state = 'closed', up_at = %s where slack_thread_id = %s """
		#updateSQL = """update app_healthcheck set alert_state = 'closed', up_at = %s, downtime_duration = %s where slack_thread_id = %s """
		cursor.execute(updateSQL, (endDowntime,getSlackThreadId))
		#cursor.execute(updateSQL, (endDowntime,getSlackThreadId, downtime_duration))


		# # get restore uptime timestamp
		getUptimeSQL = """select up_at from app_healthcheck where slack_thread_id = %s"""
		cursor.execute(getUptimeSQL, (getSlackThreadId,))
		resultUptime = cursor.fetchone()
		uptime_timestamp = resultUptime['up_at']
		up_at = datetime.strptime(uptime_timestamp, "%Y-%m-%d %H:%M:%S")

		# get downtime timestamp
		getDowntimeSQL = """select down_at from app_healthcheck where slack_thread_id = %s"""
		cursor.execute(getDowntimeSQL, (getSlackThreadId,))
		resultDowntime = cursor.fetchone()
		downtime_timestamp = resultDowntime['down_at']
		down_at = datetime.strptime(downtime_timestamp, "%Y-%m-%d %H:%M:%S")

		timeDiff = up_at - down_at
		downtime_duration = str(timeDiff)

		updateDowntimeDurationSQL = """update app_healthcheck set downtime_duration = %s where slack_thread_id = %s"""
		cursor.execute(updateDowntimeDurationSQL, (downtime_duration,getSlackThreadId))

		

		db.commit()

		

		# send slack message
		slackBlockMessageUP = [
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Service returned to Normal state :thumbsup: "
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*Application Url Healtcheck :* \n"+applicationName+ \
					"\n\n*Response Code:* \n"+responseCode+ \
					"\n\n*Back to normal at:* \n"+endDowntime+
					"\n\n*Downtime duration: * \n"+downtime_duration
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
		
		print("Duration downtime: ",str(timeDiff))


	
	return json.dumps(responseJson)

	
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000, debug=True)