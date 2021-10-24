from django.urls import path
from . import views

urlpatterns = [
    # User
    path('create/', views.UserCreateView.as_view()),
    path('<int:pk>/', views.UserDetailUpdateView.as_view()),
    path('info/', views.UserInfoView.as_view()),

    # Block List
    path('blocklist/', views.UserBlockListView.as_view()),

    # Following
    # subscribe and unsubscribe
    path('follow/', views.UserFollowView.as_view()),

    # Lenta
    path('feed/', views.FeedListView.as_view())

]