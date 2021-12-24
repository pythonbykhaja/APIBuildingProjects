from django.db import models


# Create your models here.
class Recipe(models.Model):
    """
    This class represents the Recipe Model
    """
    class Meta:
        db_table = 'recipe'

    name = models.TextField(null=False)
    description = models.CharField(max_length=256)
    number_of_servings = models.IntegerField()
    cook_time = models.IntegerField()
    direction = models.CharField(max_length=1000)
    is_publish = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}"


