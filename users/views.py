#from rest_framework_jwt.utils import jwt_payload_handler
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, UserSerializerWithToken
from django.views.generic import View
from .models import Activation, Profile
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.tokens import default_token_generator as dtg
from ITS_api import settings
from .mail_sender import send_confirm_email



class ListUsers(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserCreate(APIView):

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = UserSerializerWithToken(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(username = request.data['username'])
            Profile.objects.create(user=user, status=int(request.data['status']))

            if settings.USER_EMAIL_ACTIVATION:
                user.is_active = False
                code = dtg.make_token(user)
                act = Activation()
                act.code = code
                act.user = user
                act.save()
                user.save()
                send_confirm_email(request, user.email, code)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DetailUser(generics.RetrieveAPIView):
    permission_classes = (permissions.AllowAny,)

    queryset = User.objects.all()
    serializer_class = UserSerializer


class CurrentUserView(APIView):

    def get(self, request):
        serializer = UserSerializerWithToken(request.user)
        return Response(serializer.data)


class ConfirmEmailView(APIView):

    @staticmethod
    def get(request, code):
        act = get_object_or_404(Activation, code=code)
        user = act.user
        if user and dtg.check_token(user, code):
            user.is_active = True
            user.save()
            act.delete()
            return Response(status=status.HTTP_201_CREATED)


class ListCourseStudents(APIView):

    @staticmethod
    def get(request, courseId):
        students = User.objects.filter(coursestatistic__course_id=courseId).filter(profile__status=1)
        serializer = UserSerializer(students, many=True)
        return Response(serializer.data)
