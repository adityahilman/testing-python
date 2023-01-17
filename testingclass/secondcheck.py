from c_slack import SlackClient
from c_db import DatabaseClient
from c_resp import jsonPayload
import os
from slack_sdk import WebClient
import httpx
import asyncio
import requests
from datetime import datetime

slack_channel = os.getenv('SLACK_CHANNEL')

get_app_status_down = DatabaseClient()

async def secondCheck():
    await asyncio.sleep(3)
    app_status_down_list = get_app_status_down.getAppStatusDown()
    for all_result in app_status_down_list:
        retry_app_down = httpx.get(all_result["application_url"])

        if retry_app_down.status_code == 200:
            response_code = str(retry_app_down.status_code)
            retry_app_url = str(retry_app_down.url)
            get_app_status_down.updateAppAlertState()

            # not finished yet
            # need to create update function to database
            # get slack_thread_id from database and update alert_state to database



async def main():
	task_second_check = asyncio.create_task(secondCheck())
	await asyncio.wait([task_second_check])


if __name__ == "__main__":
	while True:
		asyncio.run(main())