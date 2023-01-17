from slack_sdk import WebClient
import os

class SlackClient:

    slack_token = os.getenv('SLACK_TOKEN')
    slackClient = WebClient(token=slack_token)
    
    def __init__(self, slack_channel, app_url, slack_thread_id):
        self.slack_channel = slack_channel
        self.app_url = app_url
        self.slack_thread_id = slack_thread_id
        #self.slack_message = self.slack_message
        

    def sendSlackDown(self):
        
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
                    }
                ]
            }
        ]

        sendSlackNotif = SlackClient.slackClient.chat_postMessage(
			channel=self.slack_channel,
			text="Service Down: "+self.app_url,
			blocks=blockMessage,
			attachments=attachmentMessage
		)

        slackThreadId = sendSlackNotif['message']['ts']
        print("Slack thread id : ", slackThreadId)

    def sendSlackUp(self):
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
    