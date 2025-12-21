from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User
from dj_rest_auth.registration.serializers import SocialLoginSerializer


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)
    user_type_display = serializers.CharField(source='get_user_type_display', read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'full_name',
            'phone', 'whatsapp', 'user_type', 'user_type_display',
            'address', 'city', 'is_verified', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'is_verified', 'created_at', 'updated_at']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        write_only=True, 
        required=True,
        style={'input_type': 'password'},
        label='Confirmer le mot de passe'
    )
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password2',
            'first_name', 'last_name', 'phone', 'whatsapp',
            'user_type', 'address', 'city'
        ]
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': False},
            'last_name': {'required': False},
        }
    
    def validate_username(self, value):
        """Vérifier que le username n'existe pas déjà"""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Ce nom d'utilisateur est déjà pris.")
        return value
    
    def validate_email(self, value):
        """Vérifier que l'email n'existe pas déjà"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Cet email est déjà utilisé.")
        return value
    
    def validate_phone(self, value):
        """Vérifier que le téléphone n'existe pas déjà"""
        if User.objects.filter(phone=value).exists():
            raise serializers.ValidationError("Ce numéro de téléphone est déjà utilisé.")
        return value
    
    def validate(self, attrs):
        """Validation globale"""
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                "password2": "Les mots de passe ne correspondent pas."
            })
        return attrs
    
    def create(self, validated_data):
        """Créer un nouvel utilisateur"""
        validated_data.pop('password2')
        password = validated_data.pop('password')
        
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        
        return user


class UpdateProfileSerializer(serializers.ModelSerializer):
    """Serializer pour la mise à jour du profil"""
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'phone', 
            'whatsapp', 'address', 'city'
        ]
        extra_kwargs = {
            'email': {'required': False},
            'phone': {'required': False},
        }
    
    def validate_email(self, value):
        """Vérifier que l'email n'est pas déjà utilisé par un autre utilisateur"""
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError("Cet email est déjà utilisé.")
        return value
    
    def validate_phone(self, value):
        """Vérifier que le téléphone n'est pas déjà utilisé par un autre utilisateur"""
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(phone=value).exists():
            raise serializers.ValidationError("Ce numéro de téléphone est déjà utilisé.")
        return value


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer pour changer le mot de passe"""
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(
        required=True, 
        write_only=True,
        validators=[validate_password]
    )
    new_password2 = serializers.CharField(required=True, write_only=True)
    
    def validate_old_password(self, value):
        """Vérifier que l'ancien mot de passe est correct"""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("L'ancien mot de passe est incorrect.")
        return value
    
    def validate(self, attrs):
        """Vérifier que les nouveaux mots de passe correspondent"""
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({
                "new_password2": "Les mots de passe ne correspondent pas."
            })
        return attrs
    
    def save(self):
        """Changer le mot de passe"""
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user

class GoogleLoginSerializer(SocialLoginSerializer):
    """
    Serializer pour accepter id_token OU access_token de Google
    """
    id_token = serializers.CharField(required=False, allow_blank=True)
    access_token = serializers.CharField(required=False, allow_blank=True)
    
    def validate(self, attrs):
        # Si id_token est fourni, l'utiliser
        if attrs.get('id_token'):
            attrs['access_token'] = attrs.get('id_token')
        
        # Vérifier qu'au moins un token est fourni
        if not attrs.get('access_token'):
            raise serializers.ValidationError(
                "Vous devez fournir soit 'access_token' soit 'id_token'"
            )
        
        return super().validate(attrs)