from slack_sdk import WebClient
from c_db import DatabaseClient
import os

class SlackClient:

    slack_token = os.getenv('SLACK_TOKEN')
    slackClient = WebClient(token=slack_token)
    slack_thread_id = ""
    

    def __init__(self, app_url:str=None, incident_time: str=None, slack_channel=None, response_code=None, slack_thread_id=None):
        self.app_url = app_url
        self.incident_time = incident_time
        self.slack_channel = slack_channel
        self.response_code = response_code
        self.slack_thread_id = slack_thread_id
        

    #def sendSlackDown(self, app_url, incident_time:str, slack_channel):
    def sendSlackDown(self):
        # self.app_url = app_url
        # self.incident_time = incident_time
        # self.slack_channel = slack_channel

        blockMessage = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ":redalert: Service Down :redalert:"
                }
            }
            
        ]

        attachmentMessage = [
            {
                "color": "#fc0303",
                "fields": [
                    {
                        "title": "Application URL Healthcheck",
                        "value": self.app_url
                    },
                    {
                        "title": "Response Code",
                        "value": self.response_code
                    },
                    {
                        "title": "Incident Time",
                        "value": self.incident_time
                    }
                ]
            }
        ]

        sendSlackNotif = SlackClient.slackClient.chat_postMessage(
			channel=self.slack_channel,
			text="Service Down",
			blocks=blockMessage,
			attachments=attachmentMessage
		)

        self.slack_thread_id = sendSlackNotif['message']['ts']
        


    def sendSlackUp(self, app_url, incident_time, slack_channel, slack_thread_id):
        self.app_url = app_url
        self.incident_time = incident_time
        self.slack_channel = slack_channel

        # slack_token = os.getenv('SLACK_TOKEN')
        # slackClient = WebClient(token=slack_token)
        blockMessage = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Service returned to normal state"
                }
            }
            
        ]

        attachmentMessage = [
            {
                "color": "#00d919",
                "fields": [
                    {
                        "title": "Application URL Healthcheck",
                        "value": self.app_name
                    }
                ]
            }
        ]

        sendSlackNotif = SlackClient.slackClient.chat_update(
			channel=self.slack_channel,
			text="Service Recovered: "+self.app_name,
            ts=self.slack_thread_id,
			blocks=blockMessage,
			attachments=attachmentMessage
		)
    