# accounts/serializers.py

from rest_framework import serializers
from .models import *


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
    
# accounts/serializers.py

class CalculationInputSerializer(serializers.Serializer):
    dob = serializers.DateField()
    premium = serializers.FloatField()
    term = serializers.IntegerField()
    frequency = serializers.CharField()
    sum_assured = serializers.FloatField()

class CalculationResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calculation
        fields = "__all__"