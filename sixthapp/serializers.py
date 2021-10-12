from django.shortcuts import get_object_or_404
from rest_framework import serializers
from sixthapp.models import WatchList, StreamingPlatform, Review
from django.contrib.auth.models import User


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"


class WatchListSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = WatchList
        fields = "__all__"
        depth = 1


class StreamingPlatformSerializers(serializers.ModelSerializer):
    watchlist = WatchListSerializer(many=True, read_only=True)

    class Meta:
        model = StreamingPlatform
        fields = "__all__"


# Some useless code..
# watchlist = serializers.PrimaryKeyRelatedField(allow_null=True, queryset=WatchList.objects.all(), required=True)
# user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True)
# movie_id = serializers.IntegerField(required=True)
# def create(self, validated_data):
#     print("validated data {}".format(validated_data))
#     watchlist = validated_data.pop("watchlist")
#     validated_data["watchlist"] = watchlist
#     # return Review.objects.create(**validated_data)