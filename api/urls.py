from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserLogoutView, UserProfileView , PostListView, PostDetailView , PostLikeView, PostCommentView ,FollowUserView, UnfollowUserView

urlpatterns = [
    path('auth/register/', UserRegistrationView.as_view(), name='register'),
    path('auth/login/', UserLoginView.as_view(), name='login'),
    path('auth/logout/', UserLogoutView.as_view(), name='logout'),
    path('users/<int:pk>/', UserProfileView.as_view(), name='user-profile'), 
    path('posts/', PostListView.as_view(), name='post-list-create'), # URL for listing and creating posts
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'), 
     path('posts/', PostListView.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:pk>/like/', PostLikeView.as_view(), name='post-like'), # URL for liking a post
    path('posts/<int:pk>/comment/', PostCommentView.as_view(), name='post-comment'), 
     path('users/<int:pk>/follow/', FollowUserView.as_view(), name='user-follow'), # URL for following a user
    path('users/<int:pk>/unfollow/', UnfollowUserView.as_view(), name='user-unfollow'),
]