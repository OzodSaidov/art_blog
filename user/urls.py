from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

app_name = 'user'
urlpatterns = [
    # path('login/', views.LoginView.as_view(), name='login')
    path('login/', LoginView.as_view(template_name='login/index.html',
                                     redirect_authenticated_user=True), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('register/', views.UserRegisterView.as_view(), name='register'),
]
