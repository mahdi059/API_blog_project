from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from .serializers import RegisterSerializer
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status



class RegisterView(APIView):
    def post(self, request):
        ser_data = RegisterSerializer(data=request.data)  
        if ser_data.is_valid():
            user = ser_data.save()  
           
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            return Response({
                'user': ser_data.data, 
                'access_token': access_token, 
                'refresh_token': refresh_token  
            }, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)
