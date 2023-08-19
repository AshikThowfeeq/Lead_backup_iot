from django.contrib import admin

from .models import Classroom,Bulb,Status,MotionDetection


admin.site.register(Classroom)
admin.site.register(Bulb)
admin.site.register(Status)
admin.site.register(MotionDetection)