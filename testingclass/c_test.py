from slack_sdk import WebClient
import os

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

    def __init__(self, app_url=None, slack_thread_id=None, alert_state=None, incident_time=None, recovered_time=None ):
        self.app_url = app_url
        self.slack_thread_id = slack_thread_id
        self.alert_state = alert_state
        self.incident_time = incident_time
        self.recovered_time = recovered_time
        self.f_test()

    def f_test(self):
        print("from test class db: ",self.app_url, self.slack_thread_id, self.alert_state, self.incident_time)
