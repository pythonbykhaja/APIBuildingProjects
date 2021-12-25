from rest_framework.generics import RetrieveUpdateAPIView, ListCreateAPIView, RetrieveAPIView
from api_instacook.models import Recipe
from api_instacook.serializers import RecipeListSerializer, RecipePublishSerializer, RecipeUnPublishSerializer, \
    RecipeDetailSerializer


# Create your views here.
class RecipeListAPIView(ListCreateAPIView):
    """
    This class represents the List view of recipes
    """

    queryset = Recipe.objects.all().filter(is_publish=True, is_deleted=False)
    serializer_class = RecipeListSerializer


class RecipePublishView(RetrieveUpdateAPIView):
    serializer_class = RecipePublishSerializer
    queryset = Recipe.objects.all().filter(is_publish=False, is_deleted=False)
    lookup_field = "id"


class RecipeUnPublishView(RetrieveUpdateAPIView):
    serializer_class = RecipeUnPublishSerializer
    queryset = Recipe.objects.all().filter(is_publish=True, is_deleted=False)
    lookup_field = "id"


class RecipeDetailView(RetrieveAPIView):
    queryset = Recipe.objects.all().filter(is_publish=True, is_deleted=False)
    lookup_field = "id"
    serializer_class = RecipeDetailSerializer

