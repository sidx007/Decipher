from django.urls import path
from . import views

app_name = "bot_home"

urlpatterns = [
    path('', views.chatbot_view, name="chatbot_view"),
    path('success/', views.success_view, name="success_view"),
    path('pages/', views.pages_view, name="pages_view"),
]
