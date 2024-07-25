from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from .models import BlogPost
from .serializers import BlogPostSerializer
from rest_framework.views import APIView
# Create your views here.

class BlogPostListCreate(generics.ListCreateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    
    # Borra todos los posts
    def delete(self,request,*args, **kwargs):
        BlogPost.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Me deja entrar a un especifico post y puedo hacerle de todo, actualizarlo, borrarlo o simplemente traerlo
class BlogPostRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    lookup_field='pk'


# Una vista customizada donde pido el query parametro title y filtro por el title blogposts/search/?title=titulodelpost
class BlogPostList(APIView):
    def get(self,request,format=None):
        
        title =  request.query_params.get("title","")
        
        if title:
            blog_posts = BlogPost.objects.filter(title__icontains= title)
        else:
            blog_posts = BlogPost.objects.all()
            
        serializer = BlogPostSerializer(blog_posts,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, format=None):
        title = request.query_params.get("title", "")
        if not title:
            return Response({"error": "Title query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        blog_post = get_object_or_404(BlogPost, title__icontains=title)
        serializer = BlogPostSerializer(blog_post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        title = request.query_params.get("title", "")
        if not title:
            return Response({"error": "Title query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        blog_post = get_object_or_404(BlogPost, title__icontains=title)
        blog_post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)