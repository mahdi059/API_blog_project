from rest_framework import serializers
from django.contrib.auth.models import User


class RegisterSerializer(serializers.ModelSerializer):
    password_check = serializers.CharField(write_only=True , required=True)
    class Meta:
        model = User
        fields = ('username','email','password', 'password_check')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        del validated_data['password_check']
        return User.objects.create_user(**validated_data)
    
    def validate(self , data):
        if data['password'] != data['password_check']:
            raise serializers.ValidationError('password must match')
        return data


