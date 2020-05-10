import requests
from django.shortcuts import render, redirect
from . models import City
from . forms import CityForm

def home(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=55b4b4c88b888425414522c90d905795'
   
    error_message=''
    message = ''
    message_class = ''


    if request.method=='POST':
        form = CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data['name']
            city_already_exists_count = City.objects.filter(name=new_city).count()
            if city_already_exists_count==0:
                r = requests.get(url.format(new_city)).json()
                if r['cod'] == 200:
                    form.save()
                else:
                    error_message = 'This city does not exist in the world!'
            else:
                error_message = 'This city already exists in the database!'

        if error_message:
            message = error_message
            message_class = 'is-danger'
        else:
            message = 'City added successfully!'
            message_class = 'is-success'

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

    context = {
        
        'weather_data': weather_data,
        'form': form,
        'message': message,
        'message_class': message_class,
    }

    return render(request, 'weather/weather.html', context)

def delete_city(request, city_name):
    City.objects.get(name = city_name).delete()

    return redirect('home')