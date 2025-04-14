from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserLogoutView, UserProfileView

urlpatterns = [
    path('auth/register/', UserRegistrationView.as_view(), name='register'),
    path('auth/login/', UserLoginView.as_view(), name='login'),
    path('auth/logout/', UserLogoutView.as_view(), name='logout'),
    path('users/<int:pk>/', UserProfileView.as_view(), name='user-profile'), 
]