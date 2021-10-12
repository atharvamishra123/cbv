from django.db import models

# Create your models here.


class Student(models.Model):
    name = models.CharField(max_length=50)


class Profile(models.Model):
    address = models.CharField(max_length=50)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)