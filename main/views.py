from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from .serializers import BlogSerializers, CommentSerializers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrReadOnly
from rest_framework import status
from .models import Blog, BlogAccess, Comment, Favorite
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Q


class CraeteBlogView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        ser_data = BlogSerializers(data=request.data)
        if ser_data.is_valid():
            ser_data.save()

            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UpdateBlogView(APIView):
    permission_classes= [IsAuthenticated, IsOwnerOrReadOnly]

    def put(self, request, pk):
        blog = Blog.objects.get(pk=pk)
        self.check_object_permissions(request, blog)
        ser_data = BlogSerializers(instance=blog, data=request.data, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_200_OK)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)
    

class DeleteBlogView(APIView):
    permission_classes= [IsAuthenticated, IsOwnerOrReadOnly]

    def delete(self, request, pk):
        blog = Blog.objects.get(pk=pk)
        blog.delete()
        return Response({'message' : 'blog deleted'}, status=status.HTTP_200_OK)
    

class GrantAccessToUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        giver = request.user
        
        if giver.id == user_id:
            return Response({"detail": "You cannot grant access to yourself."}, status=status.HTTP_400_BAD_REQUEST)
        
        receiver = get_object_or_404(User, id=user_id)

        if BlogAccess.objects.filter(giver=giver, receiver=receiver).exists():
            return Response({"detail": "Access has already been granted to this user."}, status=status.HTTP_400_BAD_REQUEST)

        BlogAccess.objects.create(giver=giver, receiver=receiver, approved=True)

        return Response({"detail": "Access granted to the user."}, status=status.HTTP_200_OK)


class ListBlogView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
      
        blogs = Blog.objects.filter(private_blog=False)
        private_blogs = Blog.objects.filter(private_blog=True)
        user_private_blogs = Blog.objects.filter(private_blog=True, user=request.user)

        accessible_blogs = []
        for blog in private_blogs:
            if BlogAccess.objects.filter(giver=blog.user, receiver=request.user, approved=True).exists():
                accessible_blogs.append(blog)
       
        blogs = list(blogs) + accessible_blogs + list(user_private_blogs)
        ser_data = BlogSerializers(instance=blogs, many=True)

        return Response(ser_data.data)


class RetrieveBlogView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        # blog = Blog.objects.get(pk=pk)
        blog = get_object_or_404(Blog, pk=pk)
        user = request.user

        if blog.private_blog and not (blog.user == user or BlogAccess.objects.filter(giver=blog.user, receiver=user, approved=True).exists()):

            return Response({"detail": "You do not have permission to view this blog."}, status=status.HTTP_403_FORBIDDEN)
        
        ser_blog = BlogSerializers(blog)

        comments = Comment.objects.filter(blog=blog)
        ser_comment = CommentSerializers(comments, many=True)

        response_data = {
            'blog':ser_blog.data,
            'comment':ser_comment.data
        }

        return Response(response_data, status=status.HTTP_200_OK)



class CreateCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        ser_data = CommentSerializers(data=request.data)
        user = request.user

        if ser_data.is_valid():
            blog = ser_data.validated_data.get("blog") 

        
            if not blog.private_blog or BlogAccess.objects.filter(giver=blog.user, receiver=user, approved=True).exists():
                ser_data.save(user=user)
                return Response(ser_data.data, status=status.HTTP_201_CREATED)
            return Response({"detail": "You do not have permission to comment no this blog."}, status=status.HTTP_403_FORBIDDEN)

        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    
class UpdateCommentView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    def put(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        self.check_object_permissions(request, comment)
        ser_data = CommentSerializers(instance=comment, data=request.data, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_200_OK)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteCommentView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def delete(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        comment.delete()
        return Response({'message' : 'comment deleted'}, status=status.HTTP_200_OK)
    

class AddBlogToFavoriteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, blog_id):
        
        user = request.user
        
     
        try:
            blog = Blog.objects.get(id=blog_id)
        except Blog.DoesNotExist:
            return Response({"detail": "Blog not found."}, status=status.HTTP_404_NOT_FOUND)
        
        if blog.private_blog:
            if not BlogAccess.objects.filter(giver=blog.user, receiver=user, approved=True).exists():
                return Response({"detail": "You do not have permission to favorite this blog."}, status=status.HTTP_403_FORBIDDEN)
            
        favorite, created = Favorite.objects.get_or_create(user=user, blog=blog)
           
        if not created:
            return Response({"detail": "Already in favorites."}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"detail": "Blog added to favorites."}, status=status.HTTP_201_CREATED)
    

class RemoveFavoriteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, blog_id):
        
        user = request.user

        try:
            favorite = Favorite.objects.get(user=user, blog=blog_id)
            favorite.delete()
            return Response({"detail": "Blog removed from favorites."}, status=status.HTTP_204_NO_CONTENT)
        
        except Favorite.DoesNotExist:
            return Response({"detail": "Blog not found in favorites."}, status=status.HTTP_404_NOT_FOUND)



class SearchBlogView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = request.GET.get("q", "").strip()  
        user = request.user

        if not query: 
            return Response({"detail": "Please provide a search query."}, status=status.HTTP_400_BAD_REQUEST)

       
        blogs = Blog.objects.filter(title__icontains=query)

        
        accessible_blogs = blogs.filter(
            Q(private_blog=False) |  
            Q(user=user) |  
            Q(BlogAccess__receiver=user, BlogAccess__approved=True)
        ).distinct()

        serialized_blogs = BlogSerializers(accessible_blogs, many=True)

        return Response(serialized_blogs.data, status=status.HTTP_200_OK)
