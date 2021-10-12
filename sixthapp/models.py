from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save


# Create your models here.
class WatchList(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    active = models.BooleanField(default=False)
    release_date = models.DateTimeField(auto_now_add=True)
    # total_reviews = models.IntegerField(default=0, null=False)
    # average_rating = models.FloatField(default=0, null=False)
    platform = models.ForeignKey("StreamingPlatform", null=True, on_delete=models.CASCADE, related_name="watchlist")


class StreamingPlatform(models.Model):
    name = models.CharField(max_length=50)
    about = models.CharField(max_length=50)
    url_field = models.URLField(max_length=200)


class Review(models.Model):
    watchlist = models.ForeignKey(WatchList, null=True, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.CharField(max_length=200, null=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="user")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.rating)


#########################################################################################################
# Learning Signals
#########################################################################################################

# Pre-Defined Signals(Model Signals)
def save_post(sender, instance, **kwargs):
    print("Post save executed..")


def save_pre(sender, instance, **kwargs):
    print("Pre save executed..")


post_save.connect(save_post, sender=StreamingPlatform)
pre_save.connect(save_pre, sender=StreamingPlatform)


