from django.db import models

# Create your models here.


# from djmoney.models.fields import MoneyField

from django.db import models
from django.utils import timezone
import uuid

# from my_library.users.models import User


class User(models.Model):
    name = models.CharField(max_length=50)


class Library(models.Model):
    address = models.CharField(max_length=255)
    librarian = models.OneToOneField('User',
                                     related_name='library',
                                     on_delete=models.CASCADE)


class Book(models.Model):
    library = models.ForeignKey(Library,
                                related_name='books',
                                on_delete=models.CASCADE)

    public_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=500)


class BookBorrow(models.Model):
    book = models.ForeignKey(Book,
                             related_name='book_borrows',
                             on_delete=models.CASCADE)
    user = models.ForeignKey(User,
                             related_name='book_borrows',
                             on_delete=models.CASCADE)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True)
    returned = models.BooleanField(default=False)

    class Meta:
        unique_together = ('book', 'user', 'start_date',)
