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
            'direction',
            'number_of_servings'
        ]


class RecipeDetailSerializer(serializers.ModelSerializer):
    """
    This implements the serialization of individual recipe
    """
    class Meta:
        model = Recipe
        fields = [
            'name',
            'description',
            'number_of_servings',
            'cook_time',
            'direction',
            'is_publish',
            'created_at',
            'updated_at',
            'is_deleted'

        ]

    def create(self, validated_data):
        return Recipe.objects.create(**validated_data)



