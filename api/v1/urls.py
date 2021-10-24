from django.urls import path, include
from user.token import MyTokenObtainPairView
from rest_framework_simplejwt import views

urlpatterns = [
    path('auth/token/', MyTokenObtainPairView.as_view()),
    path('auth/token/refresh/', views.TokenRefreshView.as_view()),
    path('user/', include('api.v1.user.urls')),
    path('post/', include('api.v1.post.urls')),
    path('comment/', include('api.v1.comment.urls')),
]
