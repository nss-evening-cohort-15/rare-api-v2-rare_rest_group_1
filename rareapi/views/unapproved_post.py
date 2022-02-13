"""View module for handling requests about games"""
from pickle import TRUE
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers,status
from rest_framework.permissions import IsAdminUser
from rareapi.models import Post,RareUser,Category, post
from rest_framework.decorators import permission_classes
from rest_framework.decorators import action, permission_classes

@permission_classes([IsAdminUser])
class UnapprovedPostView(ViewSet):
    
    """Rare posts"""
    def list(self, request):
        
        # Get all game records from the database
        posts = Post.objects.all() 
        posts = posts.filter(category__id=1)

        serializer = UnapprovedPostSerializer(
            posts, many=True, context={'request': request})
        return Response(serializer.data)     

class UnapprovedPostSerializer(serializers.ModelSerializer):
    """JSON serializer for posts

    Arguments:
        serializer type
    """
    class Meta:
        model = Post
        fields = ('id', 'title', 'publication_date', 'image_url',
                  'rareuser', 'content','approved','category')
        depth = 1