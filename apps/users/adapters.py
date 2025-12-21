from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.utils import perform_login
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    Adapter personnalisé pour gérer la création d'utilisateurs via OAuth
    """
    
    def pre_social_login(self, request, sociallogin):
        """
        Connecte automatiquement un utilisateur si l'email existe déjà
        """
        # Si l'utilisateur est déjà authentifié, ne rien faire
        if sociallogin.is_existing:
            return
        
        # Essayer de récupérer l'email
        try:
            email = sociallogin.account.extra_data.get('email', '').lower()
        except:
            return
        
        if not email:
            return
        
        # Chercher un utilisateur avec cet email
        try:
            user = User.objects.get(email=email)
            # Connecter le compte social à l'utilisateur existant
            sociallogin.connect(request, user)
        except User.DoesNotExist:
            pass
    
    def populate_user(self, request, sociallogin, data):
        """
        Peuple les données de l'utilisateur lors de la création
        """
        user = super().populate_user(request, sociallogin, data)
        
        # Extraire les données du provider
        extra_data = sociallogin.account.extra_data
        
        # Google
        if sociallogin.account.provider == 'google':
            user.first_name = extra_data.get('given_name', '')
            user.last_name = extra_data.get('family_name', '')
            user.email = extra_data.get('email', '')
            user.is_verified = extra_data.get('email_verified', False)
        
        # Facebook
        elif sociallogin.account.provider == 'facebook':
            user.first_name = extra_data.get('first_name', '')
            user.last_name = extra_data.get('last_name', '')
            user.email = extra_data.get('email', '')
            user.is_verified = True  # Facebook vérifie toujours les emails
        
        # Générer un username unique à partir de l'email
        if not user.username and user.email:
            base_username = user.email.split('@')[0]
            username = base_username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1
            user.username = username
        
        # Champ phone requis dans notre modèle, mettre une valeur par défaut
        if not user.phone:
            user.phone = None  # Sera complété plus tard par l'utilisateur
        
        return user
    
    def save_user(self, request, sociallogin, form=None):
        """
        Sauvegarde l'utilisateur avec les données complètes
        """
        user = super().save_user(request, sociallogin, form)
        
        # Marquer comme vérifié
        user.is_verified = True
        user.save()
        
        return user