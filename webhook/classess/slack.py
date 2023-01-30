import slack_sdk 
import os

class SlackClient:

    slack_token = os.getenv('SLACK_TOKEN')
    slack_client_token = slack_sdk.WebClient(token=slack_token)
    slack_channel = os.getenv('SLACK_CHANNEL')

    def __init__(self) -> None:
        pass

    def slack_notif_invalidate_cf(self, slack_user_id, timestamp, url):
        self.slack_user_id = slack_user_id
        self.timestamp = timestamp
        self.url = url

        blockMessage = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "New Invalidation Request"
                }
            }
        ]

        attachmentMessage = [
            {
                "color": "#00d919",
                "fields": [
                    {
                        "title": "Triggered by",
                        "value": "<@"+ self.slack_user_id + ">"
                    },
                    {
                        "title": "When",
                        "value": self.timestamp
                    },
                    {
                        "title": "Object Path",
                        "value": self.url
                    }
                ]
            }
        ]

        send_slack_notif = SlackClient.slack_client_token.chat_postMessage(
            channel=SlackClient.slack_channel,
            text="New Invalidation Request: "+self.url,
            blocks=blockMessage,
            attachments=attachmentMessage
        )