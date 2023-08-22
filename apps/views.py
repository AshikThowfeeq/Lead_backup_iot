from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Classroom, Bulb,Status,MotionDetection
import threading,requests
from django.views.generic import View,CreateView,FormView,TemplateView,ListView,UpdateView
from apps.forms import RegistrationForm,LoginForm
from django.contrib.auth.models import User
import requests
from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache


Userver = "blr1.blynk.cloud"


class SignUpView(CreateView):
    model=User
    form_class=RegistrationForm
    template_name="register.html"
    success_url=reverse_lazy("login")


class LoginView(FormView):
    form_class=LoginForm
    template_name="login.html"

    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")

            usr=authenticate(request,username=uname,password=pwd)
            
            if usr:
                
                login(request,usr)
                return redirect("index")
                
            else:
                 return render(request,"login.html",{"form":form})


# def login(request):
#     if request.method == 'POST':
#         username = request.POST.get('user')
#         password = request.POST.get('password')
#         if (username == 'Lead@Head' and password == '1234') or \
#                 (username == 'Lead@Control' and password == '1234') or \
#                 (username == 'Grow@Dev' and password == '1234'):
#             request.session['username'] = username
#             return redirect('index/')
#         else:
#             error_message = "Invalid Login"
#             return render(request, 'login.html', {'error_message': error_message})

#     return render(request, 'login.html')

def fetch_status(status, status_data):
    url = f"https://{Userver}/external/api/get?token={status.token}&pin={status.pin}"
    response = requests.get(url)
    fetched_status = response.text
    status_data.append({'id': status.id, 'status': fetched_status})


    # Update the status in the database
    status.status = fetched_status
    status.save()

@login_required
def index(request):
    classrooms = Classroom.objects.all()

    status_data = []

    threads = []
    for classroom in classrooms:
        statuss = Status.objects.filter(classroom=classroom)

        for sts in statuss:
            thread = threading.Thread(target=fetch_status, args=(sts, status_data))
            thread.start()
            threads.append(thread)
            

    # Wait for all threads to complete
    for thread in threads:
        thread.join()
        

    context = {
        'classrooms': classrooms,
        'status_data': status_data

    }

    return render(request, 'index.html', context)

@login_required
def bulb_control(request):
    classrooms = Classroom.objects.all()
    motion = MotionDetection.objects.all()

    status_data = []

    threads = []
    for classroom in classrooms:
        statuss = Status.objects.filter(classroom=classroom)

        for sts in statuss:
            thread = threading.Thread(target=fetch_status, args=(sts, status_data))
            thread.start()
            threads.append(thread)

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    context = {
        'classrooms': classrooms,
        'status_data': status_data,
        'motion': motion
    }

    return render(request, 'bulb_control.html', context)

# Rest of the code remains the same...



def update_pin(request, bulb_id):
    if request.method == 'POST':
        pin = request.POST.get('pin')
        status = request.POST.get('status')
        token = request.POST.get('token')

        # Update the bulb status
        bulb = get_object_or_404(Bulb, id=bulb_id)
        bulb.status = 1 if status.lower() == 'on' else 0
        bulb.save()

        # Send API request to update the physical bulb
        url = f"https://{Userver}/external/api/update?token={token}&{pin}={bulb.status}"
        requests.get(url)
        print(url)

        
        
        return JsonResponse({}, status=204)
    
def update_pin_motion(request, motionDetection_id):
    if request.method == 'POST':
        pin = request.POST.get('pin')
        status = request.POST.get('status')
        token = request.POST.get('token')

        # Update the motion detection status
        motion_detection = get_object_or_404(MotionDetection, id=motionDetection_id)
        motion_detection.status = 1 if status.lower() == 'on' else 0
        motion_detection.save()

        # Send API request to update the physical motion detection
        url = f"https://{Userver}/external/api/update?token={token}&{pin}={motion_detection.status}"
        requests.get(url)
        print(url)

    return JsonResponse({}, status=204)

class LogoutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("login")