import requests
from model import bot
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
			site_dict[site_name]['county'] = site['county']
			site_dict[site_name]['sitename'] = site['sitename']
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

