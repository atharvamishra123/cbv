from django.db import models


# Create your models here.
class Person(models.Model):
    name = models.CharField(max_length=50)


class House(models.Model):
    house_number = models.CharField(max_length=50)
    person = models.ManyToManyField(Person)
