from django.shortcuts import redirect, render,get_object_or_404
from django.contrib import messages
import requests
from decouple import config
from pprint import pprint
from .models import City
# Create your views here.
def index(request):
    cities = City.objects.all();
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric'
    
    
   #pprint(content)
   #pprint(content['id'])
    u_city = request.GET
    u_city = request.GET.get('name')
    print(u_city)
    if u_city:
        response= requests.get(url.format(u_city,config('API_KEY')))
        print(response.status_code)
        if response.status_code == 200:
            content = response.json()
            pprint(content)
            r_city = content['name']
            if City.objects.filter(name = r_city):
                messages.warning(request, 'City is already been in db')
            else:
                City.objects.create(name=r_city)
                messages.success(request,'City successfully registered')
        else:
            messages.warning(request,'City not found') 
        return redirect('indexpage')           
    city_data = []
    
    for city in cities:
        print(city)
        response= requests.get(url.format(city,config('API_KEY')))
        #! turn in into to dictionary to consume in python
        content = response.json()
        #?will pass everythin to a dictionary
        data = {
            'city' : city,
            'temp' :content['main']['temp'],
            'desc' : content['weather'][0]['description'],
            'icon' :content['weather'][0]['icon'],
        }
        city_data.append(data)
        pprint(city_data)
    context = {
        'city_data':city_data
    }    
    return render(request,'app/index2.html',context)

def city_delete(request,id):
    city = get_object_or_404(City,id=id)
    city.delete()
    messages.success(request,'City Deleted')
    return redirect('indexpage')           