from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Classroom, Bulb,Status,MotionDetection
import threading,requests

import requests
Userver = "blr1.blynk.cloud"
def login(request):
    if request.method == 'POST':
        username = request.POST.get('user')
        password = request.POST.get('password')
        if (username == 'Lead@Head' and password == '1234') or \
                (username == 'Lead@Control' and password == '1234') or \
                (username == 'Grow@Dev' and password == '1234'):
            request.session['username'] = username
            return redirect('index/')
        else:
            error_message = "Invalid Login"
            return render(request, 'login.html', {'error_message': error_message})

    return render(request, 'login.html')

def fetch_status(status, status_data):
    url = f"https://{Userver}/external/api/get?token={status.token}&pin={status.pin}"
    response = requests.get(url)
    fetched_status = response.text
    status_data.append({'id': status.id, 'status': fetched_status})


    # Update the status in the database
    status.status = fetched_status
    status.save()

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