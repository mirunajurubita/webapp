from myapp import EmployeeViews
from myapp.EmployeeViews import viewActiveTasks
from rest_framework import permissions
from rest_framework.response import Response
from django.contrib.auth import login
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
import jwt
from rest_framework.decorators import api_view
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User, Employee, Tasks
import  datetime
from django.dispatch import receiver

from .serializers import userSerializer, employeeSerializer, taskSerializer, LoginSerializer
from rest_framework.generics import ListAPIView, GenericAPIView
from .models import User, Employee, Tasks
from knox.models import AuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAdminUser


class UserRecordView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, format=None):
        users = User.objects.all()
        serializer = userSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = userSerializer(data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            serializer.create(validated_data=request.data)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                "error": True,
                "error_msg": serializer.error_messages,
            },
            status=status.HTTP_400_BAD_REQUEST
        )
class RegisterAPI(APIView):
    def post(self, request):
        serializer = userSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginAPI(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
        return response


@api_view(['GET'])
class seeActiveTasks(ListAPIView):
    queryset = Tasks.objects.filter(is_active = 1)
    serializer_class = taskSerializer
    #permission_classes = [IsAuthenticated]

    def get_queryset(self):   
        print(self.request.user)        
        print(self.request.user.id)                  # added string
        #return super().get_queryset().filter(user=self.request.user.id)
        return super().get_queryset().filter(request.user.id)
