from django.urls import path
from . import views

urlpatterns = [
    path('',views.login,name='login'),
    path('index/',views.index,name='index'),
    path('bulb/<int:bulb_id>/update/', views.update_pin, name='update_pin'),
    path('bulbs/',views.bulb_control,name="bulb_control"),
    path('motion-detection/<int:motionDetection_id>/update/', views.update_pin_motion, name='update_pin_motion'),

]