from django.urls import path
from api_instacook import views

urlpatterns = [
    path('list/', views.RecipeListAPIView.as_view(), name='recipe_list'),
    path('create/', views.RecipeCreateApiView.as_view(), name='recipe_create'),
]