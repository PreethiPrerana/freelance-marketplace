from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .serializers import RegisterSerializer, MarketplaceTokenSerializer
@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
 s=RegisterSerializer(data=request.data); s.is_valid(raise_exception=True); u=s.save(); return Response({"id":str(u.id),"email":u.email,"username":u.username,"role":u.role},status=status.HTTP_201_CREATED)
class TokenView(TokenObtainPairView): serializer_class=MarketplaceTokenSerializer
class RefreshView(TokenRefreshView): pass
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request): return Response({"id":str(request.user.id),"email":request.user.email,"username":request.user.username,"role":request.user.role})
