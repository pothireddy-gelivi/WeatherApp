from django.shortcuts import render,redirect
from app.forms import *
from django.http import HttpResponse,HttpResponseRedirect
import requests
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
# Create your views here.

def home(request):
    if request.session.get('username'):
        username = request.session.get('username')
        context = {'username':username}
        return render(request,'home.html',context)
    return render(request,'home.html')

def registration(request):
    uf=UserForm()
    pf=ProfileForm()
    context = {'uf':uf,'pf':pf}

    if request.method=='POST' and request.FILES:
        UFD=UserForm(request.POST)
        PFD=ProfileForm(request.POST,request.FILES)
        if UFD.is_valid() and PFD.is_valid():
            UFO=UFD.save(commit=False)
            password=UFD.cleaned_data['password']
            UFO.set_password(password)
            UFO.save()

            PFO=PFD.save(commit=False)
            PFO.profile_user=UFO
            PFO.save()

           
            return HttpResponseRedirect(reverse('user_login'))
    return render(request,'registration.html',context)

def user_login(request):
    if request.method=='POST':
        username=request.POST['un']
        password=request.POST['pw']
        user=authenticate(username=username,password=password)

        if user and user.is_active:
            login(request,user)
            request.session['username']=username
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponse('u r not an authenticated user')
    return render(request,'user_login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

@login_required
def profile_display(request):
    un=request.session.get('username')
    UO=User.objects.get(username=un)
    PO=Profile.objects.get(profile_user=UO)
    context = {'UO':UO,'PO':PO}
    return render(request,'profile_display.html',context)


@login_required
def change_password(request):
    if request.method=='POST':
        pw=request.POST['password']

        un=request.session.get('username')
        UO=User.objects.get(username=un)

        UO.set_password(pw)
        UO.save()
        return HttpResponse('succssfully changed your password')
    return render(request,'change_password.html')

def reset_password(request):
    if request.method=='POST':
        un=request.POST['un']
        pw=request.POST['pw']

        LUO=User.objects.filter(username=un)

        if LUO:
            UO=LUO[0]
            UO.set_password(pw)
            UO.save()
            return HttpResponse('password reset is done')
        else:
            return HttpResponse('user is not present in my DB')
    return render(request,'reset_password.html')


@login_required
def search(request):
    if request.method=='POST':
        city_name=request.POST['city']
        api_key = '14849c938001e98e24a854c796a96a00'
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}'
        response = requests.get(url)
        weather_data = response.json()
        print(weather_data)
        temperature = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        weather=weather_data['main']['feels_like']
        speed=weather_data['wind']['speed']
        username=request.session.get('username')
        LUO=User.objects.get(username=username)
        obj=WeatherData.objects.get_or_create(username=LUO,city=city_name, temperature=temperature, humidity=humidity,weather=weather, speed=speed)[0]
        obj.save()
        context = {'obj':obj}
        return render(request,'search.html',context)
    return render(request,'search.html')

@login_required
def user_history(request):
    username=request.session['username']
    UO=User.objects.get(username=username)
    LWO=WeatherData.objects.filter(username=UO)

    context = {'LWO':LWO}
    return render(request,'user_history.html',context)

def all_history(request):
    LWO=WeatherData.objects.all()
    context={'LWO':LWO}
    return render(request,'all_history.html',context)

def edit_profile(request):
    PO = request.user.profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=PO)
        if form.is_valid():
            form.save()
            return redirect('profile_display')
    else:
        form = ProfileForm(instance=PO)

    return render(request, 'edit_profile.html', {'form': form})