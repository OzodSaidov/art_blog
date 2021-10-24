from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.PostListView.as_view()),
    path('create/', views.PostCreateView.as_view()),
    path('<int:pk>/', views.PostDetailUpdateView.as_view())
]