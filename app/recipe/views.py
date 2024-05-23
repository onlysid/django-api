# Views for the recipe APIs

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import Recipe
from recipe import serializers


class RecipeViewSet(viewsets.ModelViewSet):
    # View for manage recipe APIs (multiple endpoints!)
    serializer_class = serializers.RecipeSerializer # Use the serializer
    queryset = Recipe.objects.all() # Get all objects

    # View must use token authentication
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        # Retrieve recipes for authenticated user
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        # ONLY use the RecipeSerializer if the action is list (ie viewing listview)
        if self.action == 'list':
            return serializers.RecipeSerializer

        return self.serializer_class