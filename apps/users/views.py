from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Q
from .models import User
from .serializers import (
    UserSerializer, RegisterSerializer, 
    UpdateProfileSerializer, ChangePasswordSerializer
)


class RegisterView(generics.CreateAPIView):
    """
    Enregistrer un nouvel utilisateur
    
    POST /api/users/register/
    Body: {
        "username": "john_doe",
        "email": "john@example.com",
        "password": "SecurePass123!",
        "password2": "SecurePass123!",
        "phone": "+237690000000",
        "first_name": "John",
        "last_name": "Doe",
        "city": "Douala"
    }
    """
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Générer les tokens JWT
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'Inscription réussie !',
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)


class ProfileView(generics.RetrieveUpdateAPIView):
    """
    Consulter et modifier son profil
    
    GET /api/users/profile/
    PUT/PATCH /api/users/profile/
    """
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UpdateProfileSerializer
        return UserSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    Connexion avec email, username ou téléphone
    
    POST /api/users/login/
    Body: {
        "username": "john_doe" ou "john@example.com" ou "+237690000000",
        "password": "SecurePass123!"
    }
    """
    identifier = request.data.get('username') or request.data.get('email') or request.data.get('phone')
    password = request.data.get('password')
    
    if not identifier or not password:
        return Response(
            {'error': 'Identifiant (email/username/téléphone) et mot de passe requis'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # Chercher par username, email OU téléphone
        user = User.objects.filter(
            Q(username=identifier) | Q(email=identifier) | Q(phone=identifier)
        ).first()
        
        if not user:
            return Response(
                {'error': 'Utilisateur introuvable'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Vérifier le mot de passe
        if not user.check_password(password):
            return Response(
                {'error': 'Mot de passe incorrect'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Vérifier si l'utilisateur est actif
        if not user.is_active:
            return Response(
                {'error': 'Ce compte a été désactivé'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Générer les tokens JWT
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'Connexion réussie !',
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': f'Erreur serveur: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    Déconnexion (blacklist le refresh token)
    
    POST /api/users/logout/
    Body: {
        "refresh": "refresh_token_here"
    }
    """
    try:
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response(
                {'error': 'Refresh token requis'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        token = RefreshToken(refresh_token)
        token.blacklist()
        
        return Response(
            {'message': 'Déconnexion réussie'}, 
            status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response(
            {'error': f'Erreur lors de la déconnexion: {str(e)}'}, 
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password_view(request):
    """
    Changer son mot de passe
    
    POST /api/users/change-password/
    Body: {
        "old_password": "OldPass123!",
        "new_password": "NewPass123!",
        "new_password2": "NewPass123!"
    }
    """
    serializer = ChangePasswordSerializer(
        data=request.data, 
        context={'request': request}
    )
    
    if serializer.is_valid():
        serializer.save()
        return Response(
            {'message': 'Mot de passe modifié avec succès'}, 
            status=status.HTTP_200_OK
        )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_stats_view(request):
    """
    Statistiques de l'utilisateur
    
    GET /api/users/stats/
    """
    user = request.user
    
    # Import ici pour éviter les imports circulaires
    from apps.orders.models import Order
    
    orders = Order.objects.filter(user=user)
    
    stats = {
        'total_orders': orders.count(),
        'pending_orders': orders.filter(status='pending').count(),
        'completed_orders': orders.filter(status='delivered').count(),
        'cancelled_orders': orders.filter(status='cancelled').count(),
        'total_spent': sum(
            order.total for order in orders.exclude(status='cancelled')
        ),
    }
    
    return Response(stats)