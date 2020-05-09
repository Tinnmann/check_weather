import requests
from django.shortcuts import render
from . models import City
from . forms import CityForm

def home(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metrics&appid=55b4b4c88b888425414522c90d905795'
   
    error_message=''
    
    if request.method=='POST':
        form = CityForm(request.POST)

        if form.isvalid():
            new_city = form.cleaned_data['name']
            city_already_exists_count = City.objects.filter(name=new_city).count()
            if city_already_exists_count==0:
                form.save()
            else:
                error_message = 'City already exists in the database!'

    form = CityForm()


    cities = City.objects.all()

    weather_data = []

    for city in cities:
        r = requests.get(url.format(city)).json()
        city_weather = {
            'city': city.name,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
        }
        weather_data.append(city_weather)

    print(weather_data)

    context = {'weather_data': weather_data, 'form': form}

    return render(request, 'weather/weather.html', context)
