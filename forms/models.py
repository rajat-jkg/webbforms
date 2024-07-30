from django.db import models
from django.contrib.auth.models import User


class WebbForm(models.Model):
    form_name = models.CharField(max_length=150)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customCSS = models.TextField()
    formSchema=models.TextField()
    success_message = models.TextField(default='')
    emailRecieptsEnabled = models.BooleanField(default=False)
    headerEnabled = models.BooleanField(default=True)

class Responses(models.Model):
    timesTamp = models.DateTimeField(auto_now_add=True)
    response = models.TextField()
    form = models.ForeignKey(WebbForm, on_delete=models.CASCADE)