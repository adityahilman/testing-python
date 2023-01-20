from slack_sdk import WebClient
import os
from datetime import datetime

class SlackTest():
    slack_token = os.getenv('SLACK_TOKEN')
    slackClient = WebClient(token=slack_token)

    def __init__(self, app_url=None, incident_time=None):
        self.app_url = app_url
        self.incident_time = incident_time
        self.sendslack()
        
    def sendslack(self):

        #print(self.app_url, self.incident_time)
        slacknotif = SlackTest.slackClient.chat_postMessage(
            channel="G01E624R14Z",
            text=self.app_url+self.incident_time
        )

        self.slack_thread_id = slacknotif['message']['ts']
        #self.slack_thread_id = "11111"

class Test():

    var1 = ""

    def __init__(self, app_url=None, incident_time:str=None, slack_channel=None, response_code=None):
        self.app_url = app_url
        self.incident_time = incident_time
        self.slack_channel = slack_channel
        self.response_code = response_code

    def first_test(self):
        self.var1 = SlackTest.slack_token
        #print(self.var1)
        

    def second_test(self, app_url=None, incident_time:str=None, slack_channel=None, response_code=None):
        self.app_url = app_url
        self.incident_time = incident_time
        self.slack_channel = slack_channel
        self.response_code = response_code
        print(self.app_url, self.incident_time, self.slack_channel, self.response_code)


