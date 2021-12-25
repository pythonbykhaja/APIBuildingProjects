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


class RecipePublishBaseSerializer(serializers.ModelSerializer):
    """
    This class will help for publishing and un publishing recipes
    """
    class Meta:
        model = Recipe
        fields = ['is_publish']

    is_publish = True

    def update(self, instance, validated_data):
        """
        This method will update the record
        """
        instance.is_publish = self.is_publish
        instance.save()
        return instance


class RecipePublishSerializer(RecipePublishBaseSerializer):
    is_publish = True


class RecipeUnPublishSerializer(RecipePublishBaseSerializer):
    is_publish = False


class RecipeDetailSerializer(serializers.ModelSerializer):

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