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

# @permission_classes([IsAdminUser])
class PostView(ViewSet):
    #Marking extra actions for routing
    @action(detail=False,permission_classes = [IsAdminUser])
    def unapproved(self, request):
        unapproved = Post.objects.all().filter(category__id=1)

        serializer = PostSerializer(unapproved, many=True)
        return Response(serializer.data)
        
    """Rare posts"""
    def list(self, request):
        
        # Get all game records from the database
        posts = Post.objects.all() 

        # Support filtering posts by category
        #    http://localhost:8000/posts?category=1
        #
        # That URL will retrieve all tabletop posts
        category_num = self.request.query_params.get('category', None)
        if category_num is not None:
            posts = posts.filter(category__id=category_num)

        serializer = PostSerializer(
            posts, many=True, context={'request': request})
        return Response(serializer.data)     
    
    def retrieve(self, request, pk=None):
        
        """Handle GET requests for single post

        Returns:
            Response -- JSON serialized post instance
        """
        
        try:
            # `pk` is a parameter to this function, and
            # Django parses it from the URL route parameter
            #   http://localhost:8000/posts/2
            #
            # The `2` at the end of the route becomes `pk`
            post = Post.objects.get(pk=pk)
            serializer = PostSerializer(post, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
    
    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized a post instance
        """

        # Uses the token passed in the `Authorization` header
        rareuser = RareUser.objects.get(user=request.auth.user)
        #category = Category.objects.get(pk=request.data["categoryId"])
        # Create a new Python instance of the Post class
        # and set its properties from what was sent in the
        # body of the request from the client.
        post = Post()
        post.title = request.data["title"]

        post.publication_date = request.data["publicationDate"]
        post.image_url = request.data["imageUrl"]
        post.rareuser = rareuser
        post.content = request.data["content"]
        post.approved = False
    
        category = Category.objects.get(pk=request.data["categoryId"])
        post.category = category

        try:
            post.save()
            serializer = PostSerializer(post, context={'request': request})
            return Response(serializer.data)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)
       
    def update(self, request, pk=None):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """
        rareuser = RareUser.objects.get(user=request.auth.user)
        category = Category.objects.get(pk=request.data["categoryId"])
        # Do mostly the same thing as POST, but instead of
        # creating a new instance of Post, get the game record
        # from the database whose primary key is `pk`
        post = Post.objects.get(pk=pk)
        post.rareuser = rareuser
        # post.category = request.data["category"]
        post.title = request.data["title"]
        post.publication_date = request.data["publicationDate"]
        post.image_url = request.data["imageUrl"]
        post.content = request.data["content"]
        post.approved = False
        post.category = category
        post.save()
        # 204 status code means everything worked but the
        # server is not sending back any data in the response
        return Response({}, status=status.HTTP_204_NO_CONTENT)


    def delete(self, request, pk=None):
        """Handle DELETE requests for a single game

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            post = Post.objects.get(pk=pk)
            post.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Post.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PostSerializer(serializers.ModelSerializer):
    """JSON serializer for posts

    Arguments:
        serializer type
    """
    class Meta:
        model = Post
        fields = ('id', 'title', 'publication_date', 'image_url',
                  'rareuser', 'content','approved','category')
        depth = 1