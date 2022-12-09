from flask import Flask, render_template, request
import boto3
import json
import datetime
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

slackToken = os.environ.get("xoxb-xxxx")
slackClient = WebClient(token=slackToken)
slackClientToken = WebClient(token="xoxb-xxx")



awsClient = boto3.client(
    'cloudfront',
    aws_access_key_id="xxxxx",
    aws_secret_access_key="xxxxx"
    )

app = Flask(__name__)

@app.route('/clear-cache', methods = ['POST'] )
def getSlackBot():
    getUrl = request.form ['text']
    getCalRef = request.form['trigger_id']
    getSlackChannel = request.form['channel_id']
    getSlackUser = request.form['user_id']

    # --- function invalidate ke CF --- #
    createInvalidation = awsClient.create_invalidation(
            DistributionId = "XXXXX",
            InvalidationBatch = {
                'Paths' : {
                    'Quantity' : 1,
                    'Items' : [
                        getUrl
                    ]
                },
                'CallerReference': getCalRef
            }
        )
        
    getDate = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    slackBlockMessage = [
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "New Invalidation Request :white_check_mark:"
			}
		},
		{
			"type": "section",
			"fields": [
				{
					"type": "mrkdwn",
					"text": "*Created by:*\n<@"+ getSlackUser + ">"
				}
			]
		},
		{
			"type": "section",
			"fields": [
				{
					"type": "mrkdwn",
					"text": "*When:*\n" + getDate
				}
			]
		},
		{
			"type": "section",
			"fields": [
				{
					"type": "mrkdwn",
					"text": "*Object Paths:*\n" + getUrl
				}
			]
		}
	]
    replySlack = slackClientToken.chat_postMessage(
        channel=getSlackChannel,
        text="Invalidation Successfull",
        blocks=slackBlockMessage
    )
    #print(getUrl)


    return (getUrl)
    #return replySlack

@app.route('/', methods=['GET'])
def mainRoute():
    return render_template('index.html')

@app.route('/getid', methods=['GET'])
def getId():
    return render_template('getid.html')

@app.route('/resultid', methods=['POST'])
def getResultId():
    #getId = request.form['txtId']
    getDistributionId = awsClient.get_invalidation(
        DistributionId = "xxxx",
        Id = request.form['txtId']
    )
    return(getDistributionId)
    
    #return(getDistributionId)

@app.route('/submit_invalidation', methods=['POST'])
def getCreateInvalidation():
    getCalRef = datetime.datetime.now().strftime("%H:%m:%s")
    getUrl = request.form['txtUrl']
    createInvalidation = awsClient.create_invalidation(
        DistributionId = "xxxx",
        InvalidationBatch = {
            'Paths' : {
                'Quantity' : 1,
                'Items' : [
                    getUrl
                ]
            },
            'CallerReference': getCalRef
        }
    )
    return(createInvalidation)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)