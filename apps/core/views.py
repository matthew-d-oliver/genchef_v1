import requests
import json
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Create your views here.
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Recipe, RecipePrompt
from .forms import RecipePromptForm  # Define this form for the /menu page

#rest-framework packages
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

# Constants for Lambda endpoints
GENERATE_RECIPE_LAMBDA = "https://neg7rh9vsj.execute-api.us-east-2.amazonaws.com/Testy/generate_recipe"

@method_decorator(csrf_exempt, name='dispatch')
class FetchAIContentView(APIView):
    """
    Handles the API call to the Lambda function for recipe generation.
    """
    def post(self, request, *args, **kwargs):
        print("=== FetchAIContentView Debug START ===")
        print(f"Request method: {request.method}")
        print(f"Request content type: {request.content_type}")
        print(f"Request data: {request.data}")
        print(f"Request body: {request.body}")
        
        try:
            form_data = request.data
            print(f"Form data extracted: {form_data}")

            # Prepare the payload for Lambda
            payload = {
                "usr": request.user.username if request.user.is_authenticated else "guest",
                "task": "get_options",
                "ingredients": {
                    "title": form_data.get("title"),
                    "produce": form_data.get("produce"),
                    "protein": form_data.get("protein"),
                    "carb": form_data.get("carb"),
                    "dish_style": form_data.get("dish_style"),
                    "cuisine": form_data.get("cuisine"),
                },
            }
            
            print(f"Payload prepared: {payload}")
            print(f"Lambda endpoint: {GENERATE_RECIPE_LAMBDA}")

            # Call the Lambda function
            print("Making request to Lambda...")
            response = requests.post(GENERATE_RECIPE_LAMBDA, json=payload, timeout=30)
            
            print(f"Lambda response status: {response.status_code}")
            print(f"Lambda response headers: {dict(response.headers)}")
            print(f"Lambda response text: {response.text}")
            
            if response.status_code == 200:
                response_data = response.json()
                print(f"Lambda response JSON: {response_data}")
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                error_msg = f"Lambda returned {response.status_code}: {response.text}"
                print(f"Lambda error: {error_msg}")
                return Response({"error": error_msg}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        except requests.RequestException as e:
            error_msg = f"Request exception: {str(e)}"
            print(error_msg)
            return Response({"error": error_msg}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            error_msg = f"Unexpected exception: {str(e)}"
            print(error_msg)
            import traceback
            traceback.print_exc()
            return Response({"error": error_msg}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            print("=== FetchAIContentView Debug END ===")

def menu(request):
    """Handles the /menu form and generates recipe options."""
    if request.method == "POST":
        form = RecipePromptForm(request.POST)
        if form.is_valid():
            # Save the prompt data for reference
            prompt = form.save()

            # Call Lambda to generate recipe options
            # removed extra set up brackets whih could be needed for lambda
            payload = {
                
                "body": {
                    "usr": "usr_input",
                    "task": "get_recipe",
                    "ingredients": {
                        "title": prompt.title,
                        "produce": prompt.produce,
                        "protein": prompt.protein,
                        "carb": prompt.carb,
                        "dish_style": prompt.dish_style,
                        "cuisine": prompt.cuisine,
                        }
                    }
            }
            response = requests.post(GENERATE_RECIPE_LAMBDA, json=payload)
            if response.status_code == 200:
                options = response.json().get("options", [])
                return render(request, "recipe_options.html", {"options": options, "prompt_id": prompt.id})
            else:
                return render(request, "menu.html", {"form": form, "error": "Failed to fetch recipe options."})
    else:
        form = RecipePromptForm()

    return render(request, "menu.html", {"form": form})

def recipe_detail(request, recipe_id):
    """Displays a full recipe on /recipe/####."""
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return render(request, "recipe_detail.html", {"recipe": recipe})


def recipe_options(request, prompt_id):
    """Handles recipe option selection and fetches the full recipe."""
    if request.method == "POST":
        selected_option = request.POST.get("selected_option")
        prompt = get_object_or_404(RecipePrompt, id=prompt_id)

        # Call Lambda to fetch full recipe details
        payload = {
            "body": {
                "option": selected_option,
                "prompt_data": {
                    "title": prompt.title,
                    "produce": prompt.produce,
                    "protein": prompt.protein,
                    "carb": prompt.carb,
                    "dish_style": prompt.dish_style,
                    "cuisine": prompt.cuisine,
                }
            }
        }
        response = requests.post(GENERATE_RECIPE_LAMBDA, json=payload)
        if response.status_code == 200:
            recipe_data = response.json()
            recipe = Recipe.objects.create(
                title=recipe_data.get("title"),
                description=recipe_data.get("description"),
                ingredients=recipe_data.get("ingredients"),
                instructions=recipe_data.get("instructions"),
                user=request.user if request.user.is_authenticated else None,
            )
            return redirect("recipe_detail", recipe_id=recipe.id)
        else:
            return JsonResponse({"error": "Failed to fetch full recipe details."}, status=500)

    return JsonResponse({"error": "Invalid request."}, status=400)