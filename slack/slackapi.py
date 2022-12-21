import json
import datetime
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


slack_token = os.getenv('SLACK_TOKEN')

slackClient = WebClient(token=slack_token)

generateThreadId = datetime.datetime.now().strftime("%H%m%s")

def slackMessage():
    slackThread = []
    slackBlockMessage = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": ":redalert: Thread Title"
            }
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": "Thread message 1" 
                }
            ]
        }
    ]

    slackBlockMessageReplyThread = [
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": ":white_check_mark: Thread reply 1" 
                }
            ]
        }
    ]
    sendSlackNotif = slackClient.chat_postMessage(
        channel="xxxx",
        text="Thread Slack",
        blocks=slackBlockMessage
    )

    slackThread = sendSlackNotif['message']['ts']

    sendSlackReplyThread = slackClient.chat_postMessage(
        channel="xxxx",
        thread_ts=slackThread,
        text="Thread Slack",
        blocks=slackBlockMessageReplyThread
    )

    print(slackThread)
    return generateThreadId

def testIf():
    slackThread = []
    alertState = input("Status: ")
    if alertState == "ok":
        slackThread = "slack thread id"
        print (slackThread)
    else:
        slackThread = "slack thread else"
        print (slackThread)

testIf()
#slackMessage()