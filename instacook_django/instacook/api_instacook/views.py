from rest_framework import generics

from api_instacook.models import Recipe
from api_instacook.serializers import RecipeListSerializer


# Create your views here.
class RecipeListAPIView(generics.ListCreateAPIView):
    """
    This class represents the List view of recipes
    """

    queryset = Recipe.objects.all().filter(is_publish=True, is_deleted=False)
    serializer_class = RecipeListSerializer



