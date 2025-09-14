from django.urls import path
from django.views.generic import TemplateView
from . import views
from .views import FetchAIContentView, menu, recipe_detail, recipe_options

urlpatterns = [
    path('', TemplateView.as_view(template_name="home.html"), name='home'),
    path('about/', TemplateView.as_view(template_name="about.html"), name='about'),
    path('menu/', views.menu, name='menu'),  # Use your custom menu view
    path('signup/', TemplateView.as_view(template_name="signup.html"), name='signup'),
    path('recipe/<int:recipe_id>/', recipe_detail, name='recipe_detail'),
    path('recipe_options/<int:prompt_id>/', recipe_options, name='recipe_options'),
path('user/profile', TemplateView.as_view(template_name="user/profile.html"), name='user_profile'),
    path('api/fetch-ai-content/', FetchAIContentView.as_view(), name='fetch_ai_content'),
]
