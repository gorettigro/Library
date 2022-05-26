from csv import unregister_dialect
from distutils.command.upload import upload
from operator import mod
import django
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta

# Create your models here.
class Book(models.Model):
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn = models.PositiveIntegerField()
    category = models.CharField(max_length=50)
    publisher = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name) + " ["+str(self.isbn)+']'

class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_on = models.CharField(max_length=10, blank=True)
    phone = models.CharField(max_length=10, blank=True)
    image = models.ImageField(upload_to="", blank=True)

    def __str__(self):
        return str(self.user) + " ["+str(self.roll_on)+']'

class IssuedBook(models.Model):
    member_id = models.CharField(max_length=100, blank=True)
    isbn = models.CharField(max_length=13)
    issued_date = models.DateField(auto_now=True)
    @classmethod
    def expiry():
        return datetime.today() + timedelta(days=14)
    expiry_date = models.DateField(default=expiry)
