from flask import Flask, render_template, request

from datetime import datetime
from classess.db import DatabaseClient
from classess.slack import SlackClient
from classess.aws import AwsClient


app = Flask(__name__)


aws_client = AwsClient()
slack_client = SlackClient()


@app.route('/', methods=['GET'])
def mainRoute():
    mainRouteJson = {
        "App Name": "Webhook Monitoring",
        "Status": "Alive"
    }
    return mainRouteJson

@app.route('/invalidate-cf', methods=['POST'])
def _invalidate_cf():
    url = request.form['text']
    slack_user_id = request.form['user_id']
    timestamp = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    print(url)
    # send request clear cache to CloudFront
    aws_client.invalidate_cache(url)
    slack_client.slack_notif_invalidate_cf(slack_user_id, timestamp, url)
    return url

@app.route('/webhook-healthcheck', methods=['POST'])
def _webhook_healthcheck():
    pass

@app.route('/application-status', methods=['GET'])
def _application_status():
    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8800, debug=True)