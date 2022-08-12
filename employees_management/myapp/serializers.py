from rest_framework import serializers
from .models  import User, Employee, Tasks
from django.contrib.auth import authenticate
from rest_framework.validators import UniqueTogetherValidator



class userSerializer(serializers.ModelSerializer):
    class Meta :
        model = User
        fields = [ 'id','password', 'username', 'email' ,'first_name', 'last_name', 'date_joined', 'is_employee', 'is_admin' ]
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class employeeSerializer(serializers.ModelSerializer):
    class Meta :
        model = Employee
        fields = [ 'id', 'user', 'address', 'created_at', 'updated_at', 'active_tasks', 'completed_tasks']

     

   

class taskSerializer(serializers.ModelSerializer):

    class Meta :
        model = Tasks
        fields = [ 'id', 'is_active', 'headline', 'body', 'assigned_at', 'closed_at', 'employee_id_id', 'deadline', 'days', 'hours', 'minutes', 'seconds', 'is_overdue',
        'user_id']

    

class LoginSerializer(serializers.Serializer):


    username = serializers.CharField(
        label="Username",
        write_only=True
    )
    password = serializers.CharField(
        label="Password",
        # This will be used when the DRF browsable API is enabled
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

