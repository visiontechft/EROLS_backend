from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, GoogleLoginSerializer
import logging

logger = logging.getLogger(__name__)


class GoogleLoginView(SocialLoginView):
    """
    Authentification via Google OAuth2
    
    POST /api/users/auth/google/
    Body: {
        "id_token": "token_from_google"  // Préféré
        OU
        "access_token": "token_from_google"
    }
    
    Returns:
    {
        "message": "Connexion Google réussie !",
        "user": {...},
        "tokens": {
            "access": "jwt_access_token",
            "refresh": "jwt_refresh_token"
        }
    }
    """
    adapter_class = GoogleOAuth2Adapter
    serializer_class = GoogleLoginSerializer  # ✅ Utiliser le serializer personnalisé
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        try:
            # Logger les données reçues (sans exposer le token complet)
            logger.info("Tentative de connexion Google")
            if 'id_token' in request.data:
                logger.debug(f"ID token reçu (début): {request.data['id_token'][:20]}...")
            elif 'access_token' in request.data:
                logger.debug(f"Access token reçu (début): {request.data['access_token'][:20]}...")
            
            # Appeler la méthode parente pour gérer l'authentification
            response = super().post(request, *args, **kwargs)
            
            # Si succès, formater la réponse avec nos tokens JWT
            if response.status_code == 200:
                user = request.user
                refresh = RefreshToken.for_user(user)
                
                logger.info(f"Connexion Google réussie pour l'utilisateur: {user.email}")
                
                return Response({
                    'message': 'Connexion Google réussie !',
                    'user': UserSerializer(user).data,
                    'tokens': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }
                }, status=status.HTTP_200_OK)
            
            return response
            
        except Exception as e:
            logger.error(f"Erreur lors de la connexion Google: {str(e)}", exc_info=True)
            return Response({
                'error': 'Échec de l\'authentification Google',
                'detail': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class FacebookLoginView(SocialLoginView):
    """
    Authentification via Facebook OAuth2
    
    POST /api/users/auth/facebook/
    Body: {
        "access_token": "token_from_facebook"
    }
    
    Returns:
    {
        "message": "Connexion Facebook réussie !",
        "user": {...},
        "tokens": {
            "access": "jwt_access_token",
            "refresh": "jwt_refresh_token"
        }
    }
    """
    adapter_class = FacebookOAuth2Adapter
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        try:
            logger.info("Tentative de connexion Facebook")
            
            # Appeler la méthode parente
            response = super().post(request, *args, **kwargs)
            
            # Si succès, formater la réponse
            if response.status_code == 200:
                user = request.user
                refresh = RefreshToken.for_user(user)
                
                logger.info(f"Connexion Facebook réussie pour l'utilisateur: {user.email}")
                
                return Response({
                    'message': 'Connexion Facebook réussie !',
                    'user': UserSerializer(user).data,
                    'tokens': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }
                }, status=status.HTTP_200_OK)
            
            return response
            
        except Exception as e:
            logger.error(f"Erreur lors de la connexion Facebook: {str(e)}", exc_info=True)
            return Response({
                'error': 'Échec de l\'authentification Facebook',
                'detail': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)