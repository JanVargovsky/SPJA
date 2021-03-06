﻿from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

#class CustomUser(User):
#    pass
class Item(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    price = models.FloatField()

    def __str__(self):
        return "{0} - {1}".format(self.name, self.price)

class TaskStatus(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    status = models.ForeignKey(TaskStatus, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default = datetime.now())
    deleted = models.BooleanField(default = False)

    def __str__(self):
        return self.text[:30] if not self.deleted else "DELETED - {0}".format(self.text[:30])

class Message(models.Model):
    user_from = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE)
    user_to = models.ForeignKey(User, related_name='receiver', on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(default = datetime.now())