from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserLogoutView, UserProfileView , PostListView, PostDetailView 

urlpatterns = [
    path('auth/register/', UserRegistrationView.as_view(), name='register'),
    path('auth/login/', UserLoginView.as_view(), name='login'),
    path('auth/logout/', UserLogoutView.as_view(), name='logout'),
    path('users/<int:pk>/', UserProfileView.as_view(), name='user-profile'), 
    path('posts/', PostListView.as_view(), name='post-list-create'), # URL for listing and creating posts
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'), 
]