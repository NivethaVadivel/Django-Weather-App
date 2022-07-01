#from pyexpat.errors import messages
from unicodedata import name
from django.shortcuts import redirect, render
from django.http import HttpResponse
# from django.core.mail import send_mail
from .form import CityForm
from .models import City
import requests
from django.contrib import messages
# Create your views here.

# def say_hello(request):
#     x =calculate()
#     return render(request, 'hello.html',{'name' : 'Achu'})

# def index(request):
#     send_mail('Hello from Nivetha',
#     'Hello there. This is an automated message.',
#     'nivethavadivel.1@gmail.com',
#     ['jejeka2731@mahazai.com'],
#     fail_silently=False)
#     return render(request,'index.html',{})

# def index1(request):
#     return render(request,"index1.html",{})

def home(request):
    url='http://api.openweathermap.org/data/2.5/weather?q={},&appid=db85d7c54bb8888aa63a43ca9cdb5996&units=metric'

    if request.method=='POST':
        form=CityForm(request.POST)
        print(form)
        if form.is_valid():
            NCity=form.cleaned_data['name']
            CCity=City.objects.filter(name=NCity).count()
            if CCity==0:
                res=requests.get(url.format(NCity)).json()
                print(res)
                if res['cod']==200:
                    form.save()
                    messages.success(request," "+NCity+" Added Successfully...!!!")
                else:
                    messages.error(request," City does not exist...!!!")
            else:
                messages.error(request," City already exists...!!!")
    
    form=CityForm()
    cities=City.objects.all()
    data=[]
    for city in cities:
        res=requests.get(url.format(city)).json()
        city_weather={
            'city':city,
            'temperature' : res['main']['temp'],
            'description' : res['weather'][0]['description'],
            'country' : res['sys']['country'],
            'icon' : res['weather'][0]['icon'],
        }
        data.append(city_weather)
    context={'data' : data,'form' : form}
    return render(request,"weatherapp.html",context)

def delete_city(request,CName):
    City.objects.get(name=CName).delete()
    messages.success(request," "+CName+" Removed Successfully...!!!")
    return redirect('Home') 