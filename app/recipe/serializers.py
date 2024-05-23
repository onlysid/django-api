# Serializers for recipe APIs

from rest_framework import serializers
from core.models import Recipe

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_minutes', 'price', 'link']
        read_only_fields = ['id']

# Extend the RecipeSerializer!
class RecipeDetailSerializer(RecipeSerializer):
    class Meta(RecipeSerializer.Meta):
        # Take the existing recipe serializer and add an additional field!
        fields = RecipeSerializer.Meta.fields + ['description']
