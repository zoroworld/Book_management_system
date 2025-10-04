from django.urls import path
from .views import RegisterView, MyTokenObtainPairView, index
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('',index, name='user_index'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', MyTokenObtainPairView.as_view(), name='login'),       # username + password
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]