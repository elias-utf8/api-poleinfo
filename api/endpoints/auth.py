"""
Routes d'authentification et gestion des tokens.

Auteur: Elias GAUTHIER
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from core.auth import verify_token
from core.security import create_access_token
from db.requests.user import authenticate_user
from models.schemas import Token

router = APIRouter(tags=["authentification"])


@router.post(
    "/token",
    response_model=Token,
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Authentification réussie",
            "content": {
                "application/json": {
                    "example": {
                        "access_token": "jwt.token.value",
                        "token_type": "bearer",
                        "user_type": "admin",
                        "user_name": "Elias Gauthier",
                        "user_login": "egauthier",
                    }
                }
            },
        },
        400: {
            "description": "Identifiants incorrects",
            "content": {"application/json": {"example": {"detail": "Identifiants incorrects"}}},
        },
        422: {"description": "Erreur de validation des données d'entrée"},
    },
)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Authentifie un utilisateur et génère un token JWT.

    Vérifie les identifiants de l'utilisateur,
    génère un token JWT si l'authentification réussit, et renvoie
    les informations nécessaires.
    """
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Identifiants incorrects")

    type_user = user["type"]
    user_login = user["login"]
    user_name = user["nom"]

    token = create_access_token(user["id_user"])
    return {
        "access_token": token,
        "token_type": "bearer",
        "user_type": type_user,
        "user_name": user_name,
        "user_login": user_login,
    }


@router.get(
    "/verify-token",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Token valide",
            "content": {"application/json": {"example": {"valid": True, "user_id": 42}}},
        },
        401: {
            "description": "Token invalide ou expiré",
            "content": {"application/json": {"example": {"detail": "Credentials invalides"}}},
        },
    },
)
def verify_token_endpoint(user_id: int = Depends(verify_token)):
    """
    Vérifie la validité d'un token JWT.

    Utilise la dépendance verify_token pour valider le token
    et récupérer l'ID de l'utilisateur.
    """
    return {"valid": True, "user_id": user_id}
