from django.urls import path
from api_instacook import views

urlpatterns = [
    path('', views.RecipeListAPIView.as_view(), name='recipe_list'),
    path('<int:id>/', views.RecipeDetailView.as_view(), name='recipe_detail'),
    path('<int:id>/publish/', views.RecipePublishView.as_view(), name='recipe_publish'),
    path('<int:id>/unpublish/', views.RecipeUnPublishView.as_view(), name='recipe_unpublish'),

]
