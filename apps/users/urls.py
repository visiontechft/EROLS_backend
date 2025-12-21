from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views
from .social_views import GoogleLoginView, FacebookLoginView

app_name = 'users'

urlpatterns = [
    # Authentification classique
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('change-password/', views.change_password_view, name='change-password'),
    path('stats/', views.user_stats_view, name='stats'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    
    # Authentification sociale (OAuth)
    path('auth/google/', GoogleLoginView.as_view(), name='google-login'),
    path('auth/facebook/', FacebookLoginView.as_view(), name='facebook-login'),
]