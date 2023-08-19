from django.db import models

class Classroom(models.Model):
    name = models.CharField(max_length=100)
    token = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Bulb(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    pin = models.CharField(max_length=100)
    status = models.IntegerField(choices=((0, 'Off'), (1, 'On')), default=0)
    token = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Status(models.Model):
    id = models.IntegerField(primary_key=True)  # Manually set the ID
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    pin = models.CharField(max_length=100)
    token = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class MotionDetection(models.Model):
    name = models.CharField(max_length=100)
    clname=models.CharField(max_length=100)
    pin = models.CharField(max_length=100)
    status = models.IntegerField(choices=((0, 'Off'), (1, 'On')), default=0)
    token = models.CharField(max_length=100)

    def __str__(self):
        return self.name