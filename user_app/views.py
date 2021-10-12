from django.views.decorators.csrf import csrf_exempt
from rest_framework import mixins, generics
from user_app.serializers import RegistrationSerializer
from rest_framework.decorators import api_view
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from user_app import models
from django.dispatch import Signal, receiver
# Create your views here.

#  https://stackoverflow.com/questions/42775784/how-can-i-serialize-a-queryset-from-an-unrelated-model-as-a-nested-serializer
# @method_decorator(csrf_exempt, name='dispatch')

custom_signal = Signal(providing_args=['name'])


class UserRegistration(mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        data = {}
        print("request.data {}".format(request.data))
        user = User.objects.filter(username=request.data['username']).first()
        data['response'] = "User Creation Successful!"
        data['username'] = user.username
        data['email'] = user.email
        token = Token.objects.get(user=user).key
        data['token'] = token
        custom_signal.send(sender=User, name='just for testing purpose')
        return Response(data)


class LogoutView(mixins.DestroyModelMixin, generics.GenericAPIView):  # Not working

    def get_object(self):
        user = self.User.objects.get(pk=self.request.user.pk)
        token = user.auth_token
        return token

    def destroy(self, request, *args, **kwargs):
        super(LogoutView, self).destroy(request, *args, **kwargs)


@receiver(custom_signal)
def func2(sender, **kwargs):
    print("user is created..")
    print("/n/n", kwargs)

# @api_view(['POST'])
# def UserRegistration(request):
#     if request.method == "POST":
#         print("request.data {}".format(request.data))
#         serializer = RegistrationSerializer(data=request.data)
#         if serializer.is_valid():
#             print("if..")
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors)


