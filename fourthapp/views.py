from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import generics
from fourthapp.serializer import BookSerializer
from fourthapp.models import BookBorrow


# Create your views here.
class UserBookListView(generics.ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        msg = {"detail": "Number of borrowed by user is Zero.."}
        id = self.kwargs['id']
        queryset = BookBorrow.objects.filter(user__id=id)
        return queryset
