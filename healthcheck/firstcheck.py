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


async def first_check():
	#time.sleep(2)
	
	getAppList = "select * from app_list where application_health_status = 1"
	cursor.execute(getAppList)
	allResult = cursor.fetchall()
	await asyncio.sleep(5)
	timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	print("------------------- ",timestamp,"------------------------")
	for appList in allResult:
		#print(appList["application_url"])
		async with httpx.AsyncClient() as client:
			getAppHealthCheck = await client.get(appList["application_url"])
		
		print("First check : ", getAppHealthCheck.url, getAppHealthCheck.status_code)
		if getAppHealthCheck.status_code != 200:
			applicationUrl = str(getAppHealthCheck.url)
			updateApplist = "update app_list set application_health_status = 0 where application_url = %s"
			cursor.execute(updateApplist, (applicationUrl,))
			db.commit()
			time.sleep(3)
			failedApp = httpx.get(applicationUrl)
			if failedApp.status_code != 200:
				responseCode = str(failedApp.status_code)
				print("retry at ",timestamp,",", applicationUrl)
				sendRequest = {
					"incident": {
						"state": "open",
						"resource": {
							"labels": {
								"host": applicationUrl,
								"response_code": responseCode,
								"timestamp": timestamp
							}
						}
					}		
				}
				postRequest = requests.post("http://localhost:8000/healthcheck-webhook", json=sendRequest)
				return postRequest
                
	print("-------------------------------------------")

	
		
async def main():
	task_first_check = asyncio.create_task(first_check())
	await asyncio.wait([task_first_check])


if __name__ == "__main__":
	while True:
		asyncio.run(main())