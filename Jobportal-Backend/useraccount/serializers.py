from dataclasses import fields
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import EmployerProfile


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password')

        extra_kwargs = {
            'first_name': { 'required': True, 'allow_blank': False },
            'last_name': { 'required': True, 'allow_blank': False },
            'email': { 'required': True, 'allow_blank': False },
            'password': { 'required': True, 'allow_blank': False, 'min_length': 6 },
        }

class UserSerializer(serializers.ModelSerializer):
    resume = serializers.CharField(source='userprofile.resume')
    class Meta:
        model = User
        fields = ('id','first_name', 'last_name', 'email', 'username', 'resume')
class EmployeeSerializer(serializers.ModelSerializer):

    company_name = serializers.CharField(source='employerprofile.company_name', allow_null=True)
    services = serializers.CharField(source='employerprofile.services', allow_null=True)
    employees = serializers.IntegerField(source='employerprofile.employees', allow_null=True)
    website = serializers.CharField(source='employerprofile.website', allow_null=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'username',  'company_name','services', 'employees', 'website')
