import asyncio
import os
import threading
import time
import uvicorn
import requests
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from model.bot import *
from model.response_response import* 
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get('/', include_in_schema=False)
async def index(request: Request):
	return FileResponse("./index.html", media_type="text/html")

@app.get('/api/siteList')
async def AOIdata():
	url = 'https://data.moenv.gov.tw/api/v2/aqx_p_432?language=zh&api_key=e1b238db-315d-4ddf-b7fb-cebd33b68c77'
	site_list = []
	try:
		result = requests.get(url).json()['records']
		for site in  result:
			site_name = site['county'] + site['sitename']
			site_list.append(site_name)
		response_site_list = response_message_200_list(
			data = site_list
    )
		return JSONResponse(status_code=200, content=response_site_list.dict())
	except Exception as e:
		response_error = response_message_error(
			error = e
    )
		return JSONResponse(status_code=500, content=response_error.dict())

@app.get('/api/site/{siteName}')
async def site_data(siteName):
	url = 'https://data.moenv.gov.tw/api/v2/aqx_p_432?language=zh&api_key=e1b238db-315d-4ddf-b7fb-cebd33b68c77'
	try:
		result = requests.get(url).json()['records']
		site_dict = {}
		for site in  result:
			site_name = site['county'] + site['sitename']
			site_dict[site_name]= {}
			site_dict[site_name]['sitename'] =  site['county'] + site['sitename']
			site_dict[site_name]['AQI'] = site['aqi']
			site_dict[site_name]['PM2.5'] = site['pm2.5']
			site_dict[site_name]['PM10'] = site['pm10']
			site_dict[site_name]['o3'] = site['o3']
			site_dict[site_name]['status'] = site['status']
			site_dict[site_name]['publishtime'] = site['publishtime']
			
		response_data = site_dict[siteName] 
		response_site_list = response_message_200_dict(
			data = response_data
    )
		return JSONResponse(status_code=200, content=response_site_list.dict())
	except Exception as e:
		print(e)
		message = str(e)
		response_error = response_message_error(
			error = message
    )
		return JSONResponse(status_code=500, content=response_error.dict())

# Create Scheduler
scheduler = BackgroundScheduler()

# Define the executing time of the schedule
def scheduled_task():
	siteName = '臺北市中山'
	url = 'https://data.moenv.gov.tw/api/v2/aqx_p_432?language=zh&api_key=e1b238db-315d-4ddf-b7fb-cebd33b68c77'
	try:
		result = requests.get(url).json()['records']
		site_dict = {}
		for site in  result:
			site_name = site['county'] + site['sitename']
			site_dict[site_name]= {}
			site_dict[site_name]['sitename'] = site['sitename'] + site['county']
			site_dict[site_name]['AQI'] = site['aqi']
			site_dict[site_name]['PM2.5'] = site['pm2.5']
			site_dict[site_name]['PM10'] = site['pm10']
			site_dict[site_name]['o3'] = site['o3']
			site_dict[site_name]['status'] = site['status']
			site_dict[site_name]['publishtime'] = site['publishtime']
			
		data = site_dict[siteName] 
		# print(data)
	except Exception as e:
		print(e)

	now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	print(f"Scheduled task executed at {now}")
	content = f'當前時間：{now}\n'
	send_discord_message(
			content,
			siteName,
			AQI=data["AQI"],
			PM25=data["PM2.5"],
			PM10=data["PM10"],
			O3=data["o3"],
			username='EMO',
			avatar_url='https://training.pada-x.com/imgs/head1.jpg'
	)

# Use CronTrigger to set up time in 7:30 am everyday
trigger = CronTrigger(hour=7, minute=30)
scheduler.add_job(scheduled_task, trigger)

@app.on_event("startup")
async def startup_event():
	start_background_thread()
	if not scheduler.running:
		print("Starting the scheduler...")
		scheduler.start()

@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down the scheduler...")
    scheduler.shutdown()

def send_request():
    url = 'https://team-aqi.onrender.com/api/site/%E5%9F%BA%E9%9A%86%E5%B8%82%E5%9F%BA%E9%9A%86'
    while True:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print(f"Request successful: {response.status_code}")
            else:
                print(f"Request failed: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
        time.sleep(300)

def start_background_thread():
    print("Starting background thread...")  # 确认后台线程启动日志
    request_thread = threading.Thread(target=send_request)
    request_thread.daemon = True  # 确保线程在主进程退出时自动退出
    request_thread.start()
    print("Background thread started.")

if __name__ == "__main__":
	print("Starting request thread...")  # 添加日志信息确认线程启动
	request_thread = threading.Thread(target=send_request)
	request_thread.daemon = True  # 确保线程在主进程退出时自动退出
	request_thread.start()

	port = int(os.environ.get("PORT", 8000))
	uvicorn.run(app, host="0.0.0.0", port=port)
# def test():
# 	siteName = '臺北市中山'
# 	url = 'https://data.moenv.gov.tw/api/v2/aqx_p_432?language=zh&api_key=e1b238db-315d-4ddf-b7fb-cebd33b68c77'
# 	try:
# 		result = requests.get(url).json()['records']
# 		site_dict = {}
# 		for site in  result:
# 			site_name = site['county'] + site['sitename']
# 			site_dict[site_name]= {}
# 			site_dict[site_name]['sitename'] = site['sitename'] + site['county']
# 			site_dict[site_name]['AQI'] = site['aqi']
# 			site_dict[site_name]['PM2.5'] = site['pm2.5']
# 			site_dict[site_name]['PM10'] = site['pm10']
# 			site_dict[site_name]['o3'] = site['o3']
# 			site_dict[site_name]['status'] = site['status']
# 			site_dict[site_name]['publishtime'] = site['publishtime']
			
# 		data = site_dict[siteName] 
# 		print(data)
# 	except Exception as e:
# 		print(e)

# 	now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
# 	print(f"Scheduled task executed at {now}")
# 	content = f'當前時間：{now}\n'
# 	# response = site_data(site_name)
# 	# data = response
# 	send_discord_message(
# 			content,
# 			siteName,
# 			AQI=data["AQI"],
# 			PM25=data["PM2.5"],
# 			PM10=data["PM10"],
# 			O3=data["o3"],
# 			username='EMO',
# 			avatar_url='https://training.pada-x.com/imgs/head1.jpg'
# 	)
# test()