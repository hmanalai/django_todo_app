from django.urls import path
from .views import TodoList, TodoDetail

urlpatterns = [
    path('api/tasks/', TodoList.as_view()),
    path('api/tasks/<int:pk>/', TodoDetail.as_view()),
]