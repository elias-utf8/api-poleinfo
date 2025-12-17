"""
Génération de tokens JWT et vérification des privilèges administrateur.

Auteur: Elias GAUTHIER
"""

from datetime import datetime, timedelta

import jwt
from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext

from config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from core.auth import verify_token
from db.requests.user import get_user_by_id

# Configuration du contexte de cryptographie utilisant l'algorithme bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Constante définissant le type d'utilisateur administrateur dans la base de données
ADMIN_TYPE = 1


def create_access_token(user_id: int):
    # Calcul de la date d'expiration du token
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # Préparation du payload du token avec l'identifiant utilisateur et la date d'expiration
    payload = {"sub": str(user_id), "exp": expire}

    # Encodage du token avec la clé secrète et l'algorithme configurés
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


async def verify_admin(user_id: int = Depends(verify_token)):
    # Récupération des informations complètes de l'utilisateur
    user = get_user_by_id(user_id)

    # Vérification des droits administrateur
    if not user or user["type"] != ADMIN_TYPE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Accès refusé: droits d'administrateur requis"
        )

    # Retour de l'identifiant utilisateur pour utilisation dans les routes protégées
    return user_id
