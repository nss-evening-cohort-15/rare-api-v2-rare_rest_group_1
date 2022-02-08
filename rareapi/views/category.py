from unicodedata import category
from webbrowser import get
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rareapi.models import Category, RareUser

class CategoryView(ViewSet):
    # permission_classes' = [IsAdminUser] has Objects.permissions
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
    
    # @action(methods=['post', 'delete'], detail=True)
        # Get all game records from the database
        categories = Category.objects.all() 

        # Support filtering posts by category
        #    http://localhost:8000/posts?category=1
        #
        # That URL will retrieve all tabletop posts
      

        serializer = CategorySerializer(
            categories, many=True, context={'request': request})
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized a category instance
        """

        # Uses the token passed in the `Authorization` header
        category = Category()
        
        # Create a new Python instance of the Post class
        # and set its properties from what was sent in the
        # body of the request from the client.
       
        category.label = request.data["label"]

    
    #     category = Category.objects.get(pk=request.data["category_id"])
    #     category.category = category

        try:
            category.save()
            serializer = CategorySerializer(category, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)
        
    def update(self, request, pk=None,  permission_classes=[IsAdminUser]):
        """Handle PUT requests for a category
        
        Returns:
            Response -- Empty body with 204 status code
        """
        if not request.auth.user.is_staff:
            return Response({}, status=status.HTTP_403_FORBIDDEN)
        
        category = Category.objects.get(pk=pk)
        category.label = request.data["label"]
        category.save()
        
        return Response({}, status=status.HTTP_204_NO_CONTENT)
        
    def destroy(self, request, pk=None,
                permission_classes=[IsAdminUser]):
        """Handle DELETE requests for a single category

        Returns:
            Response -- 200, 404, or 500 status code
        """
        if not request.auth.user.is_staff:
            return Response({}, status=status.HTTP_403_FORBIDDEN)
## this makes it so that we can only delete if we are admin/authorized
        try:
            category = Category.objects.get(pk=pk)
            category.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Category.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @action(methods=["get"], detail=False, permission_classes=[IsAdminUser])
    def test(self, request):
        return Response('It worked')




class CategorySerializer(serializers.ModelSerializer):
    """JSON serializer for categories

    Arguments:
        serializers
    """
    class Meta:
        model = Category
        fields = ( 'id', 'label')

