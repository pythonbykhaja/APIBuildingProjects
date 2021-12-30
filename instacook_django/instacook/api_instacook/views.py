from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.generics import RetrieveUpdateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, \
    CreateAPIView

from api_instacook.models import Recipe
from api_instacook.serializers import RecipeListSerializer, RecipePublishSerializer, RecipeUnPublishSerializer, \
    RecipeDetailSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django_filters import filters

UserModel = get_user_model()


# Create your views here.
class RecipeListAPIView(ListCreateAPIView):
    """
    This class represents the List view of recipes
    """

    queryset = Recipe.objects.all().filter(is_publish=True, is_deleted=False)
    serializer_class = RecipeListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name', 'description']
    filterset_fields = ['name', 'description']
    ordering_fields = ['name', 'description']


class RecipePublishView(RetrieveUpdateAPIView):
    serializer_class = RecipePublishSerializer
    queryset = Recipe.objects.all().filter(is_publish=False, is_deleted=False)
    lookup_field = "id"
    permission_classes = [IsAuthenticated]


class RecipeUnPublishView(RetrieveUpdateAPIView):
    serializer_class = RecipeUnPublishSerializer
    queryset = Recipe.objects.all().filter(is_publish=True, is_deleted=False)
    lookup_field = "id"
    permission_classes = [IsAuthenticated]


class RecipeDetailView(RetrieveUpdateDestroyAPIView):
    """
    This view will implement GET, PUT, POST, PATCH and DELETE requests
    on specific recipe
    """
    queryset = Recipe.objects.all().filter(is_publish=True, is_deleted=False)
    lookup_field = "id"
    serializer_class = RecipeDetailSerializer

    def perform_destroy(self, instance):
        """
        This method is overwritten to to perform soft delete
        """
        instance.is_deleted = True
        instance.save()


class UserAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = UserModel.objects.all()
