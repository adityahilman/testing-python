from c_slack import SlackClient
from c_db import DatabaseSelect, DatabaseUpdate
from c_resp import jsonPayload
import os
from slack_sdk import WebClient
import httpx
import asyncio
import requests
from datetime import datetime

slack_channel = os.getenv('SLACK_CHANNEL')


# get_slack_channel = SlackClient(slack_channel, app_name)
# get_slack_channel.sendSlackDown()

get_app_list = DatabaseSelect()


async def firstCheck():
    await asyncio.sleep(2)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    app_list = get_app_list.getAppList()
    for app_result in app_list:
        async with httpx.AsyncClient() as client:
            get_app_status = await client.get(app_result["application_url"])
        
        print("App  : ", get_app_status.url, get_app_status.status_code)
        if get_app_status.status_code != 200:
            print(get_app_status.url)
            app_url = str(get_app_status.url)
            # update to database
            update_app_status = DatabaseUpdate(app_url)
            update_app_status.updateAppStatus()

            # post to webhook

            jsonPost = jsonPayload(app_url, get_app_status.status_code, timestamp)
            postWebhook = requests.post("http://localhost:9000/healthcheck-webhook", json=jsonPost.jsonUp())
            return postWebhook



async def main():
	task_first_check = asyncio.create_task(firstCheck())
	await asyncio.wait([task_first_check])

if __name__ == "__main__":
	while True:
		asyncio.run(main())