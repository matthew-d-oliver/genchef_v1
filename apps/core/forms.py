from django import forms
from .models import RecipePrompt

class RecipePromptForm(forms.ModelForm):
    class Meta:
        model = RecipePrompt
        fields = ["title", "produce", "protein", "carb", "dish_style", "cuisine"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Recipe Title (optional)"}),
            "produce": forms.TextInput(attrs={"placeholder": "Produce (optional)"}),
            "protein": forms.TextInput(attrs={"placeholder": "Protein (optional)"}),
            "carb": forms.TextInput(attrs={"placeholder": "Carbs (optional)"}),
            "dish_style": forms.TextInput(attrs={"placeholder": "Dish Style (optional)"}),
            "cuisine": forms.TextInput(attrs={"placeholder": "Cuisine (optional)"}),
        }
