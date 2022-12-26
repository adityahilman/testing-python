import boto3
import json
import datetime
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from botocore.exceptions import ClientError
import httpx
import asyncio
import mysql.connector
import time

# db connector
db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_pass = os.getenv('DB_PASS')
db_name = os.getenv("DB_NAME")

db = mysql.connector.connect(
	host=db_host,
	user=db_user,
	passwd=db_pass,
	database=db_name
)
cursor = db.cursor(dictionary=True)

async def first_check():
	getAppList = "select * from list_application where application_health_status = 1"
	
	cursor.execute(getAppList)
	allResult = cursor.fetchall()
	for appList in allResult:
		#print(appList["application_url"])
		async with httpx.AsyncClient() as client:
			getAppHealthCheck = await client.get(appList["application_url"])
			#getAppHealthCheck = httpx.get(appList["application_url"])
		print(getAppHealthCheck.url,getAppHealthCheck.status_code)
		if getAppHealthCheck.status_code != 200:
			applicationUrl = str(getAppHealthCheck.url)
			updateApplist = "update list_application set application_health_status = 0 where application_url = %s"
			cursor.execute(updateApplist, (applicationUrl,))
			db.commit()
			print("call function retryAppCheck")
			
	second_check()
	return appList["application_url"]

def second_check():
	time.sleep(3)
	getRetryAppList = "select application_url from list_application where application_health_status = 0"
	cursor.execute(getRetryAppList)
	retryAllResult = cursor.fetchall()
	for retryAppList in retryAllResult:
		print(retryAppList["application_url"])
		resultAppList = httpx.get(retryAppList["application_url"])
		if resultAppList.status_code == 200:
			retryAppUrl = str(resultAppList.url)
			updateRetryApp = "update list_application set application_healh_status = 1 where application_url = %s"
			cursor.execute(updateRetryApp, (retryAppList,) )
			db.commit()
		print("=========================================")
		print("result from function retry second_check")
		print(resultAppList.url, resultAppList.status_code)
		

while True:
	asyncio.run(first_check())

#asyncio.run(appCheck())
