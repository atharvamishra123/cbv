from rest_framework import serializers
from fourthapp.models import BookBorrow


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookBorrow
        fields = "__all__"