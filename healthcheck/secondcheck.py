import os
import httpx
import asyncio
import mysql.connector
import time
import datetime
import requests



# db connector
db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_pass = os.getenv('DB_PASS')
db_name = os.getenv("DB_NAME")

db = mysql.connector.connect(
	host=db_host,
	user=db_user,
	passwd=db_pass,
	database=db_name,
	autocommit=True
)
cursor = db.cursor(dictionary=True)


async def second_check():
	
	getRetryAppList = "select application_url from app_list where application_health_status = 0"
	cursor.execute(getRetryAppList)
	retryAllResult = cursor.fetchall()
	await asyncio.sleep(5)
	timestamp = datetime.datetime.now().strftime("%H:%M:%S")

	for retryAppList in retryAllResult:

		resultAppList = httpx.get(retryAppList["application_url"])
		if resultAppList.status_code == 200:
			retryAppUrl = str(resultAppList.url)
			responseCode = str(resultAppList.status_code)
			updateRetryApp = "update app_list set application_health_status = 1 where application_url = %s"
			cursor.execute(updateRetryApp, (retryAppUrl,) )
			db.commit()
			print("2nd check - service back to normal: "+retryAppUrl)
			sendRequest = {
				"incident": {
					"state": "closed",
					"resource": {
						"labels": {
							"host": retryAppUrl,
							"response_code": responseCode,
							"timestamp": timestamp
						}
					}
				}		
			}
			postRequest = requests.post("http://localhost:8000/healthcheck-webhook", json=sendRequest)
			#print(postRequest.content)

		
		else:
			print("======================================="+timestamp)
			print("Service down after 2s : "+str(resultAppList.url))
			print("=========================================")
		
async def main():
	task_second_check = asyncio.create_task(second_check())
	await asyncio.wait([task_second_check])


if __name__ == "__main__":
	while True:
		asyncio.run(main())