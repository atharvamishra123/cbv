from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from fifthapp.views import ListCreateSnippets, DetailsView
from sixthapp.views import (WatchListAV,
                            WatchListDetailsView,
                            StreamingPlatformList,
                            StreamingPlatformDetailsView,
                            ListReviews,
                            ReviewsByMovies,
                            ReviewParticularMovie)

from user_app.views import UserRegistration, LogoutView

urlpatterns = [

    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path("listcreate/", ListCreateSnippets.as_view()),
    path("detail/<int:pk>/", WatchListDetailsView.as_view()),
    path("mymovies/", WatchListAV.as_view()),

    path("pfdetail/", StreamingPlatformList.as_view()),
    path("pf_detail/<int:pk>/", StreamingPlatformDetailsView.as_view()),
    path("allreviews/", ListReviews.as_view(), name="all_review"),
    path("reviews/<int:pk>/", ReviewsByMovies.as_view()),
    path("review/movie/<int:pk>/", ReviewParticularMovie.as_view(), name="review-particular-movie"),

    # urls for user_app
    path('register/', UserRegistration.as_view(), name="user_registration"),
    path('login/', obtain_auth_token, name='login'),
    path("logout/", LogoutView.as_view(), name="logout")
]
