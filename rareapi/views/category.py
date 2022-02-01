from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rareapi.models import Category

class CategoryView(ViewSet):
    """Rare categories"""
    def retrieve(self, request, pk=None):
        """Handle GET requests for single category

        Returns:
            Response -- JSON serialized category
        """
        try:
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(category, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):

        # Get all game records from the database
        categories = Category.objects.all() 

        # Support filtering posts by category
        #    http://localhost:8000/posts?category=1
        #
        # That URL will retrieve all tabletop posts
        categories = Category.objects.all()

        serializer = CategorySerializer(
            categories, many=True, context={'request': request})
        return Response(serializer.data)
    # def create(self, request):
    #     """Handle POST operations
    #     Returns:
    #         Response -- JSON serialized a post instance
    #     """

    #     # Uses the token passed in the `Authorization` header
    #     rareuser = RareUser.objects.get(user=request.auth.user)
        
    #     # Create a new Python instance of the Post class
    #     # and set its properties from what was sent in the
    #     # body of the request from the client.
    #     post = Post()
    #     post.title = request.data["title"]

    #     post.publication_date = request.data["publicationDate"]
    #     post.image_url = request.data["imageUrl"]
    #     post.rareuser = rareuser
    #     post.content = request.data["content"]
    #     post.approved = request.data["approved"]
    
    #     category = Category.objects.get(pk=request.data["categoryId"])
    #     post.category = category

    #     try:
    #         post.save()
    #         serializer = PostSerializer(post, context={'request': request})
    #         return Response(serializer.data)

    #     except ValidationError as ex:
    #         return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)
        




class CategorySerializer(serializers.ModelSerializer):
    """JSON serializer for categories

    Arguments:
        serializers
    """
    class Meta:
        model = Category
        fields = ( 'id', 'label')
