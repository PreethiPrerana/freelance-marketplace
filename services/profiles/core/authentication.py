"""Validate Identity-service JWTs without querying a local user table.

Each service owns its database, so these services must not use SimpleJWT's
standard get_user() lookup against a local integer-primary-key User model.
The signed JWT is verified using the shared JWT_SIGNING_KEY and its UUID
subject is exposed as a lightweight authenticated principal.
"""
from dataclasses import dataclass
from typing import Any

from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication


@dataclass(frozen=True)
class ServicePrincipal:
    id: str
    role: str
    email: str = ""
    is_authenticated: bool = True
    is_anonymous: bool = False

    @property
    def pk(self) -> str:
        return self.id


class IdentityJWTAuthentication(JWTAuthentication):
    """Authenticate a token issued by Identity without local DB user lookup."""

    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        user_id = validated_token.get("user_id")
        role = validated_token.get("role")
        if not user_id or role not in {"client", "freelancer"}:
            raise AuthenticationFailed("Token is missing a valid user identity or role.")

        principal = ServicePrincipal(
            id=str(user_id),
            role=str(role),
            email=str(validated_token.get("email", "")),
        )
        return principal, validated_token
