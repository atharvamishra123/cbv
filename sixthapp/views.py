from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from sixthapp.models import WatchList, StreamingPlatform, Review
from rest_framework.status import HTTP_404_NOT_FOUND
from sixthapp.serializers import WatchListSerializer, StreamingPlatformSerializers, ReviewSerializer
from rest_framework import mixins, generics
from rest_framework.permissions import IsAuthenticated
from django.core.signals import request_finished
from django.dispatch import receiver, Signal


class ListReviews(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    queryset = Review.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ReviewsByMovies(mixins.ListModelMixin,
                      generics.CreateAPIView,
                      generics.GenericAPIView, ):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        movie = get_object_or_404(WatchList, id=self.kwargs['pk'])
        queryset = movie.reviews.all()
        # We can also do something like this bellow..(more efficient way..)
        # pk = self.kwargs['pk']
        # return Review.objects.filter(watchlist=pk)
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ReviewParticularMovie(mixins.CreateModelMixin,
                            mixins.UpdateModelMixin,
                            generics.GenericAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    queryset = Review.objects.all()

    def post(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        movies = WatchList.objects.get(pk=pk)
        user = self.request.user.id
        user_review_queryset = Review.objects.filter(watchlist=movies, user=user)
        if user_review_queryset.exists():
            raise ValidationError("You have already reviewed this movie...")

        # request.data._mutable = True
        request.data['watchlist'] = self.kwargs["pk"]
        request.data['user'] = self.request.user.id
        print("request_data {}".format(request.data))
        return self.create(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super(ReviewParticularMovie, self).partial_update(request, *args, **kwargs)


class WatchListAV(APIView):

    def get(self, request):
        movies = WatchList.objects.all()
        serializer = WatchListSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class WatchListDetailsView(APIView):

    def get_object(self, pk):
        try:
            return WatchList.objects.get(id=pk)
        except WatchList.DoesNotExist:
            return Response({"error": "movie not found"}, status=HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        movie = self.get_object(pk)
        serializer = WatchListSerializer(movie)
        return Response(serializer.data)

    def put(self, request, pk):
        movie = self.get_object(pk)
        serializer = WatchListSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    def patch(self, request, pk):
        movie = self.get_object(pk)
        serializer = WatchListSerializer(movie, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, pk):
        movie = self.get_object(pk)
        movie.delete()


class StreamingPlatformList(APIView):

    def get(self, request):
        platform = StreamingPlatform.objects.all()
        serializer = StreamingPlatformSerializers(platform, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StreamingPlatformSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class StreamingPlatformDetailsView(APIView):

    def get_object(self, pk):
        try:
            return StreamingPlatform.objects.get(id=pk)
        except StreamingPlatform.DoesNotExist:
            return Response({"error": "movie not found"}, status=HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        movie = self.get_object(pk)
        serializer = StreamingPlatformSerializers(movie)
        return Response(serializer.data)

    def put(self, request, pk):
        movie = self.get_object(pk)
        serializer = StreamingPlatformSerializers(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    def patch(self, request, pk):
        movie = self.get_object(pk)
        serializer = StreamingPlatformSerializers(movie, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, pk):
        movie = self.get_object(pk)
        movie.delete()


###################################################################################################################
#  Learning Signals
###################################################################################################################


@receiver(request_finished)
def func(sender, **kwargs):
    print("signal from sixthapp view")
