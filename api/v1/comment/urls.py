from django.urls import path
from . import views

urlpatterns = [
    # # path('list/', ),
    path('create/', views.CommentCreateView.as_view()),
    path('<int:pk>/', views.CommentUpdateView.as_view())
]