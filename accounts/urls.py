from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views


app_name = 'accounts'
urlpatterns = [
    path('register/', views.RegisterView.as_view()),
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]





# "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MzUxNTM0NCwiaWF0IjoxNzQyNjUxMzQ0LCJqdGkiOiJiNWEyYTQ0ODBlODk0YjZjOTVmYWFjZjA2NDZkYzE2NyIsInVzZXJfaWQiOjR9.MoWHd5ROPDKCkjWwp738zxlHLDrASe6py30BtnxEvF8",
# "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQyNjUxNTI0LCJpYXQiOjE3NDI2NTEzNDQsImp0aSI6ImI5ZTRmN2I3ODdlMzRlZDM4YTk1MGU1OTNjMDEzMTBjIiwidXNlcl9pZCI6NH0.FTIKjMNkIokJZDxig1eZz-DrdV-n5osIhS-2YZyk8XI"
