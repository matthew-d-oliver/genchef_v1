from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.username

class Recipe(models.Model):
    # Basic recipe data
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name="recipes")
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    ingredients = models.JSONField(default=list)  # Store as a JSON list
    instructions = models.JSONField(default=list)  # Store as a JSON list
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title or "Untitled Recipe"

class RecipePrompt(models.Model):
    # Data for prompts to OpenAI
    title = models.CharField(max_length=200, blank=True)
    produce = models.CharField(max_length=200, blank=True)
    protein = models.CharField(max_length=200, blank=True)
    carb = models.CharField(max_length=200, blank=True)
    dish_style = models.CharField(max_length=100, blank=True)
    cuisine = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prompt on {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
