from django.shortcuts import render

from darksky import forecast
from datetime import date, timedelta, datetime

from ipstack import GeoLookup    # doesnt give accurate City name  gave Pretoria
import requests
import json


# Create your views here.

def whome(request):
	cityloc = -26.08, 27.94

	ip_request = requests.get('https://get.geojs.io/v1/ip.json')
	my_ip = ip_request.json()['ip']  # ip_request.json() => {ip: 'XXX.XXX.XX.X'}
	print(my_ip)
	geo_request_url = 'https://get.geojs.io/v1/ip/geo/' + my_ip + '.json'
	geo_request = requests.get(geo_request_url)
	geo_data = geo_request.json()


	#detailbyip = GeoLookup('e434eb3865d20898eb97fd00767afbf0')
	#geo_data = detailbyip.get_own_location()
	#print(str(geo_data))


	lat = geo_data['latitude']
	lon = geo_data['longitude']
	city = geo_data['city']
	cityloc = lat,lon
	
	
	
	
	weekday = date.today()
	
	weatherinfo = forecast('af01e6071f266c8191d8446298b7f097',*cityloc)
	
	#dayd = {}
	weekly_weather = {}
	today_weather = {}
	
	#with weatherinfo as cityl:
	for daiy in weatherinfo.daily:
		#dayd = dict(weday=date.strftime(weekday,'%a'), sum=daiy.summary, tempMin=daiy.temperatureMin, tempMax=daiy.temperatureMax)
		#print('{weday} ---- {tempMin} - {tempMax}'.format(dayd))  # Rajneesh getting NameError for weday as not defined but correctly filled in dict dayd
		#print(str(weday), ' ---- ', str(tempMin), ' - ',str(tempMax) )  # Rajneesh getting NameError for weday as not defined but correctly filled in dict dayd
		#print(str(dayd))
		#weekday += timedelta(days=1)
		pic = ''
		
		summary = daiy.summary.lower() #('{sum}'.format(dayd).lower())
		if 'drizzle' in summary:
			pic = 'rain.png'
		if 'rain' in summary:
			pic = 'rain.png'
		if 'clear' in summary:
			pic = 'sun.png'
		if 'partly cloudy' in summary:
			pic = 'partly-cloudy-day.png'
		if 'overcast' in summary:
			pic = 'partly-cloudy-day.png'
		if 'cloud' in summary:
			pic = 'clouds.png'
			
		#weekly_weather.update({'{weday}'.format(dayd): {'tempMin':'{tempMin}'.format(dayd), 'tempMax':'{tempMax}'.format(dayd), 'pic':pic }})
		
		
		weekly_weather.update({date.strftime(weekday,'%a'): {'tempMin':round(daiy.temperatureMin,1), 'tempMax':round(daiy.temperatureMax,1), 'pic':pic , 'summary':summary}})
		weekday += timedelta(days=1)
		print(str(weekly_weather))



	darkskyicon = weatherinfo.currently.icon + '.png'
	today_weather.update({'tempNow': round(weatherinfo.currently.temperature,1), 'pic':darkskyicon})
	#weekly has todays values
	#today_weather = weekly_weather[(date.strftime(date.today(),'%a'))]  
	# delete todays value to avoid duplication and html only shows 6 days of week
	del weekly_weather[(date.strftime(date.today(), '%a'))]   
	




	hour = datetime.now().hour
	hourly_weather = {}
	i=0
	while hour < 24:
		temp = round(weatherinfo.hourly[i].temperature)
		summary = weatherinfo.hourly[i].summary.lower()
		pic = ''
		if 'drizzle' in summary:
			pic = 'rain.png'
		if 'rain' in summary:
			pic = 'rain.png'
		if 'clear' in summary:
			pic = 'sun.png'
		if 'partly cloudy' in summary:
			pic = 'partly-cloudy-day.png'
		if 'overcast' in summary:
			pic = 'partly-cloudy-day.png'
		if 'cloud' in summary:
			pic = 'clouds.png'
		
		
		if hour > 12:
			hourly_weather.update({'{}PM'.format(hour-12): {'pic':pic, 'temp':temp}})
			#print('{}pm-{}'.format(hour-12,temp))
		else:
			hourly_weather.update({'{}AM'.format(hour): {'pic':pic, 'temp':temp}})
			#print('{}am-{}'.format(hour,temp))
		hour+=1
		i+=1
		print(str(hourly_weather))


	return render(request,'index.html', {'weekly_weather':weekly_weather, 'hourly_weather':hourly_weather, 'today_weather':today_weather, 'city':city})