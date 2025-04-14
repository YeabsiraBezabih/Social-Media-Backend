from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from .serializers import UserSerializer
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from .models import User
from .serializers import UserSerializer

from .models import Post
from .serializers import PostSerializer
from rest_framework import status, generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Post, Like, Comment
from .serializers import LikeSerializer, CommentSerializer
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import User, Follow

User = get_user_model() # Get the custom User model

class UserRegistrationView(APIView):
    permission_classes = [AllowAny] # Allow anyone to access this endpoint

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'User registered successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    permission_classes = [AllowAny] # Allow anyone to access login

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
                'message': 'Login successful.'
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated] # Only authenticated users can logout

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist() # Blacklist the refresh token to invalidate it
                return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'Invalid refresh token or logout failed'}, status=status.HTTP_400_BAD_REQUEST)
class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    Retrieve and update user profile.
    - GET: Retrieve user profile by user_id (pk).
    - PUT/PATCH: Update user profile by user_id (pk).
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] # Allow read for all, update for authenticated users

    def get_object(self):
        """
        Override get_object to retrieve user based on user_id from URL.
        """
        return self.queryset.get(pk=self.kwargs['pk']) # 'pk' comes from URL path parameter ':user_id'

    def perform_update(self, serializer):
        """
        Perform update action. For now, just save. You can add custom logic here if needed.
        """
        serializer.save()
        
class PostListView(generics.ListCreateAPIView):
    """
    List all posts (for now, could be modified for feeds later) & create a new post.
    - GET: List all posts.
    - POST: Create a new post (requires authentication).
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] # Allow read for all, create for authenticated users

    def perform_create(self, serializer):
        """
        Associate the current user with the newly created post.
        """
        serializer.save(user=self.request.user) # Set the user to the current authenticated user


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a specific post.
    - GET: Retrieve a post by post_id (pk).
    - PUT/PATCH: Update a post by post_id (pk) (requires authentication).
    - DELETE: Delete a post by post_id (pk) (requires authentication).
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] # Allow read for all, update/delete for authenticated users

    # You might want to add more specific permissions later, e.g., only allow post author to update/delete.
    # For MVP, IsAuthenticatedOrReadOnly is sufficient for basic protection.
    
    
class PostLikeView(APIView):
    """
    Like or unlike a post.
    - POST: Like a post (if not already liked).
    """
    permission_classes = [permissions.IsAuthenticated] # Only authenticated users can like

    def post(self, request, pk): # 'pk' here is for post_id
        post = get_object_or_404(Post, pk=pk)
        user = request.user

        # Check if the user has already liked the post
        if Like.objects.filter(user=user, post=post).exists():
            return Response({'message': 'You have already liked this post.'}, status=status.HTTP_200_OK) # Or 208 Already Reported

        like = Like.objects.create(user=user, post=post)
        serializer = LikeSerializer(like) # Serialize the newly created like (optional, for response data)
        return Response({'message': 'Post liked'}, status=status.HTTP_201_CREATED)


class PostCommentView(generics.CreateAPIView):
    """
    Create a comment on a post.
    - POST: Create a new comment on a post (requires authentication).
    """
    queryset = Comment.objects.all() # Although we are overriding perform_create, queryset is needed by CreateAPIView
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated] # Only authenticated users can comment

    def perform_create(self, serializer):
        """
        Associate the current user and post with the newly created comment.
        """
        post_pk = self.kwargs['pk'] # Get post_id from URL path parameter 'pk'
        post = get_object_or_404(Post, pk=post_pk)
        serializer.save(user=self.request.user, post=post) # Set user and post for the commen
        
        

class FollowUserView(APIView):
    """
    Follow a user.
    - POST: Follow a user by user_id (requires authentication).
    """
    permission_classes = [permissions.IsAuthenticated] # Only authenticated users can follow

    def post(self, request, pk): # 'pk' here is for following_user_id (user to be followed)
        user_to_follow = get_object_or_404(User, pk=pk) # User to be followed
        follower = request.user # Current authenticated user is the follower

        if follower == user_to_follow:
            return Response({'error': 'You cannot follow yourself.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if already following
        if Follow.objects.filter(follower=follower, following=user_to_follow).exists():
            return Response({'message': f'You are already following {user_to_follow.username}.'}, status=status.HTTP_200_OK) # Or 208 Already Reported

        follow_relation = Follow.objects.create(follower=follower, following=user_to_follow)
        return Response({'message': f'You are now following {user_to_follow.username}.'}, status=status.HTTP_201_CREATED)


class UnfollowUserView(APIView):
    """
    Unfollow a user.
    - POST: Unfollow a user by user_id (requires authentication).
    """
    permission_classes = [permissions.IsAuthenticated] # Only authenticated users can unfollow

    def post(self, request, pk): # 'pk' here is for unfollowing_user_id (user to be unfollowed)
        user_to_unfollow = get_object_or_404(User, pk=pk) # User to be unfollowed
        follower = request.user # Current authenticated user is the follower

        if follower == user_to_unfollow:
            return Response({'error': 'You cannot unfollow yourself.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if actually following before unfollowing
        follow_relation = Follow.objects.filter(follower=follower, following=user_to_unfollow).first()
        if follow_relation:
            follow_relation.delete()
            return Response({'message': f'You have unfollowed {user_to_unfollow.username}.'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': f'You are not following {user_to_unfollow.username}.'}, status=status.HTTP_200_OK) # Or 400 Bad Request if you want to indicate an error