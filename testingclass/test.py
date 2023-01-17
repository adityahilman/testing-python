from c_test import Testing, cDummy
from c_slack import SlackClient
import os

#print("app name :")
#app_name = input()
slack_channel = os.getenv('SLACK_CHANNEL')

app_url = "test app"
slackNotif = SlackClient(slack_channel, app_url, 0)
slackNotif.sendSlackDown()
