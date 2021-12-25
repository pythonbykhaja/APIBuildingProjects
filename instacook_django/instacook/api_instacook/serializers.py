from rest_framework import serializers
from api_instacook.models import Recipe


class RecipeListSerializer(serializers.ModelSerializer):
    """
    This serializer is used to serialize/deserialize the list of recipe objects
    """

    class Meta:
        model = Recipe
        fields = [
            'id',
            'name',
            'description',
            'cook_time',
            'directions',
            'num_of_servings'
        ]






