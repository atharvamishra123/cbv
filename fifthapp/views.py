from django.shortcuts import render
from rest_framework.decorators import api_view
from fifthapp.models import Snippet
from fifthapp.serializers import SnippetSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import HTTP_404_NOT_FOUND


class ListCreateSnippets(APIView):

    def get(self, request):
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)


class DetailsView(APIView):

    def get_object(self, pk):
        try:
            return Snippet.objects.get(id=pk)
        except Snippet.DoesNotExist:
            raise HTTP_404_NOT_FOUND

    def get(self, request, pk):
        print("get...")
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    def patch(self, request, pk):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, pk):
        snippet = self.get_object(pk)
        snippet.delete()

# @api_view(['GET', 'POST'])
# def ListCreateSnippets(request):
#     if request.method == 'GET':
#         snippets = Snippet.objects.all()
#         serializer = SnippetSerializer(snippets, many=True)
#         print("serializer {}".format(serializer))
#         return Response(serializer.data)
#
#     if request.method == 'POST':
#         serializer = SnippetSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#
#
# @api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
# def DetailsView(request, pk):
#     if request.method == 'GET':
#         snippets = Snippet.objects.get(id=pk)
#         serializer = SnippetSerializer(snippets)
#         return Response(serializer.data)
#
#     if request.method == 'PUT':
#         snippet = Snippet.objects.get(id=pk)
#         serializer = SnippetSerializer(snippet, data=request.data)
#         if serializer.is_valid():
#             print("if..")
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
#
#     if request.method == 'PATCH':
#         snippet = Snippet.objects.get(id=pk)
#         serializer = SnippetSerializer(snippet, data=request.data, partial=True)
#         if serializer.is_valid():
#             print("if..")
#             serializer.save()
#             return Response(serializer.data)
#
#     if request.method == 'DELETE':
#         snippet = Snippet.objects.get(id=pk)
#         snippet.delete()

