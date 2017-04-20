from django.db import models

# Create your models here.

class UserInfo(models.Model):
    username = models.CharField(max_length=40, unique=True)
    password = models.CharField(max_length=40)
    emails = models.CharField(max_length=100)




    def __str__(self):
        return self.name