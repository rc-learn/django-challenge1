from django.shortcuts import render, redirect

# Create your views here.

from note.models import Note

from darksky import forecast
from datetime import date, timedelta, datetime
import requests
import json

def homepage(request):
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
	city = str(geo_data['city']) + ', ' + str(geo_data['region'])
	cityloc = lat,lon
	#print(cityloc[0], cityloc[1])



	API_key = "37916ba68bc273b7d2ee6cfe5071a87f"
	base_url = "http://api.openweathermap.org/data/2.5/onecall?&units=metric&exclude=minutely"
	Final_url = base_url + "&appid=" + API_key + "&lat=" + str(lat) + "&lon=" + str(lon)
	weather_data = requests.get(Final_url).json()
	print(type(weather_data))
	#print(type(weather_data['daily'][0]['weather']))
	#print(weather_data['daily'][0]['weather'][0]['description'])
	
	
# using DarkSky API
	#weatherinfo = forecast('af01e6071f266c8191d8446298b7f097',*cityloc)
	



	weekly_weather = {}
	today_weather = {}
	hourly_weather = {}


	#Get next day weather 
	weekday = date.today() 
	# + timedelta(days=1)     if need from next day onwards
	print(weekday)
	i = 0
	for daiy in weather_data['daily']:
	
		pic = ''
		ani = ''
		summary = daiy['weather'][0]['description'].lower() #('{sum}'.format(dayd).lower())
		if 'drizzle' in summary:
			pic = 'rain.png'
			ani = 'rain'
		if 'rain' in summary:
			pic = 'rain.png'
			ani = 'rain'
		if 'cloudy' in summary:
			pic = 'clouds.png'
			ani = 'cloudy'
		if 'clear' in summary:
			pic = 'sun.png'
			ani = 'clear-day'
		if 'cloud' in summary:
			pic = 'partly-cloudy-day.png'
			ani = 'cloudy'
		if 'overcast' in summary:
			pic = 'partly-cloudy-day.png'
			ani = 'partly-cloudy-day'
		if 'thunderstorm' in summary:
			pic = 'rain.png'
			ani = 'rain'  
		if 'drizzle' in  summary:
			pic = 'rain.png'
			ani = 'sleet'  
		if 'snow' in  summary:
			pic = 'rain.png'
			ani = 'snow'  
		if 'mist' in  summary:
			pic = 'rain.png'
			ani = 'fog'  


		weekly_weather.update({date.strftime(weekday,'%a'): {'temp':round(daiy['temp']['day'],1), 'tempMin':round(daiy['temp']['min'],1), 'tempMax':round(daiy['temp']['max'],1), 'pic':pic , 'summary':summary, 'ani':ani}})
		weekday += timedelta(days=1)
		i += 1
		if i == 5:
			break
	#print(str(weekly_weather))




		#"clear-day", "clear-night", 
		#"partly-cloudy-day", "partly-cloudy-night", "cloudy", "rain", 
		#"fog", "sleet", "snow", "wind",
	#darkskyicon = weather_data.currently.icon + '.png'
	#today_weather.update({'tempNow': round(weather_data['current'].['temp'],1), 'pic':darkskyicon})
	
	#weekly has todays values
	today_weather = weekly_weather[(date.strftime(date.today(),'%a'))]
	today_weather['temp'] = weather_data['current']['temp']
	today_weather['clouds'] = weather_data['current']['clouds']
	today_weather['wind'] = weather_data['current']['wind_speed']
	today_weather['feel'] = round(weather_data['current']['feels_like'],1)
	# delete todays value to avoid duplication and html only shows 6 days of week but added 1 on top
	del weekly_weather[(date.strftime(date.today(), '%a'))]   
	print(str(today_weather))
	print(str(weekly_weather))


	hour = (datetime.now().hour) + 1
	i=0
	for hrw in weather_data['hourly']:
	
	#return only next 4 hours as webpage gets too lng original -> while hour < 24:
		temp = round(hrw['temp'],1)
		summary = hrw['weather'][0]['description'].lower()
		pic = ''
		if 'drizzle' in summary:
			pic = 'rain.png'
			ani = 'rain'
		if 'rain' in summary:
			pic = 'rain.png'
			ani = 'rain'
		if 'cloudy' in summary:
			pic = 'clouds.png'
			ani = 'cloudy'
		if 'clear' in summary:
			pic = 'sun.png'
			ani = 'clear-day'
		if 'cloud' in summary:
			pic = 'partly-cloudy-day.png'
			ani = 'cloudy'
		if 'overcast' in summary:
			pic = 'partly-cloudy-day.png'
			ani = 'partly-cloudy-day'
		if 'thunderstorm' in summary:
			pic = 'rain.png'
			ani = 'rain'  
		if 'drizzle' in  summary:
			pic = 'rain.png'
			ani = 'sleet'  
		if 'snow' in  summary:
			pic = 'rain.png'
			ani = 'snow'  
		if 'mist' in  summary:
			pic = 'rain.png'
			ani = 'fog'  

		
		
		if hour > 12:
			hourly_weather.update({'{}PM'.format(hour-12): {'pic':pic, 'ani':ani, 'temp':temp, 'summary':summary}})
			#print('{}pm-{}'.format(hour-12,temp))
		else:
			hourly_weather.update({'{}AM'.format(hour): {'pic':pic, 'ani':ani, 'temp':temp, 'summary':summary}})
			#print('{}am-{}'.format(hour,temp))
		hour+=1
		i+=1
		if i == 4:
			break
	print(str(hourly_weather))
















	#get note or show up like new Note
	noteid = int(request.GET.get('noteid',0))  
	#read all notes
	notes = Note.objects.all()
	
	
	# if SAVE is clicked to submit
	if request.method == 'POST':
		noteid_sub = int(request.POST.get('noteid', 0))
		name_sub = request.POST.get('name')
		datas_sub = request.POST.get('content', '')
		
		if noteid_sub > 0:
			#need to update existing
			notepage = Note.objects.get(pk=noteid_sub)
			notepage.name = name_sub
			notepage.datas = datas_sub
			notepage.save()
			#update webpage with new saved info (refreshed from DB)
			return redirect('/wenotes?noteid=%i' %noteid_sub)
		else:
			#new note need to be added
			notepage = Note.objects.create(name=name_sub, datas=datas_sub)
			#update webpage with new note from DB
			return redirect('/wenotes?noteid=%i' %notepage.id)
			
	# if existing note, point to that note id in DB
	if noteid > 0:
		notepage = Note.objects.get(pk=noteid)
	else:
		notepage = ''
	
	book = {
		'noteid': noteid,
		'notes': notes,
		'notepage' : notepage
		}
		
	return render(request, 'homepage.html', { 'book':book ,'weekly_weather':weekly_weather, 'hourly_weather':hourly_weather, 'today_weather':today_weather, 'city':city})
#	return render(request, 'homepage.html', book , {'weekly_weather':weekly_weather, 'hourly_weather':hourly_weather, 'today_weather':today_weather, 'city':city})

	

def d_note(request, noteid):
	notepage = Note.objects.get(pk=noteid)
	notepage.delete()
	#refresh webpage and open empty note
	return redirect('/wenotes?noteid=0')
