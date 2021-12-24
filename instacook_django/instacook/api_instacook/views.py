from django.shortcuts import render
from rest_framework import generics
from api_instacook.serializers import RecipeListSerializer, RecipeDetailSerializer
from api_instacook.models import Recipe


# Create your views here.
class RecipeListAPIView(generics.ListAPIView):
    """
    This class represents the List view of recipes
    """

    queryset = Recipe.objects.all()
    serializer_class = RecipeListSerializer


class RecipeCreateApiView(generics.CreateAPIView):
    serializer_class = RecipeDetailSerializer
    queryset = Recipe.objects.all()

