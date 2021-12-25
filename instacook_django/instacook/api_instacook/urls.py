from django.urls import path
from api_instacook import views

urlpatterns = [
    path('', views.RecipeListAPIView.as_view(), name='recipe_list'),

]