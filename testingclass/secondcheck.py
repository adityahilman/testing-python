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

db_client = DatabaseClient()

async def secondCheck():
    await asyncio.sleep(2)
    recovered_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    app_status_down_list = db_client.getAppStatusDown()
    for all_result in app_status_down_list:
        retry_app_down = httpx.get(all_result["application_url"])
        print("Service down : ", retry_app_down.url, retry_app_down.status_code)

        if retry_app_down.status_code == 200:
            app_url = str(retry_app_down.url)
            # update application_health_status to 1 (healthy)
            print("Service back to normal : ", retry_app_down.url)

            db_client.updateAppStatus(app_url, "1")
            response_code = str(retry_app_down.status_code)
            
            # get slack_thread_id from database 
            get_slack_thread_id = db_client.getSlackThreadId(app_url)
            for result_slack_thread_id in get_slack_thread_id:
                slack_thread_id = result_slack_thread_id["slack_thread_id"]
                # incident_time = result_slack_thread_id['incident_at']
            
            print("slack thread id from secondcheck: ", slack_thread_id)
            # update alert_state to database
            # db_client.updateAppAlertState(app_url, slack_thread_id, str(recovered_time))
            

            # post to webhook
            jsonPost = jsonPayload(app_url, response_code, str(recovered_time))
            jsonPost.jsonUp()




async def main():
	task_second_check = asyncio.create_task(secondCheck())
	await asyncio.wait([task_second_check])


if __name__ == "__main__":
	while True:
		asyncio.run(main())