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

    def validate_num_of_servings(self, value):
        """
        Validates num of servings
        """
        if value < 1:
            raise serializers.ValidationError('Number of servings must be greater than 0.')
        if value > 50:
            raise serializers.ValidationError('Number of servings must not be greater than 50. ')
        return value

    def validate_cook_time(self, value):
        """
        This method validates the cook time
        :param value: value of the Cook time
        :return: Validation Errors if validation fails
        """
        if value < 1:
            return serializers.ValidationError('Cook time must be greater than 0. ')
        if value > 300:
            return serializers.ValidationError('Cook time cannot be greater than 300. ')
        return value


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
