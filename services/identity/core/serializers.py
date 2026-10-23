from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
User=get_user_model()
class RegisterSerializer(serializers.ModelSerializer):
 password=serializers.CharField(write_only=True, min_length=10)
 class Meta: model=User; fields=("id","username","email","password","role")
 def create(self, validated_data):
  return User.objects.create_user(**validated_data)
class MarketplaceTokenSerializer(TokenObtainPairSerializer):
 username_field = User.EMAIL_FIELD
 @classmethod
 def get_token(cls, user):
  token=super().get_token(user); token["role"]=user.role; token["email"]=user.email; return token
