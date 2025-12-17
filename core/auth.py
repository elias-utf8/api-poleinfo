"""
Authentification et vérification des tokens JWT.

Auteur: Elias GAUTHIER
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from config import ALGORITHM, SECRET_KEY
from db.requests.user import get_user_by_id

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_token(token: str = Depends(oauth2_scheme)) -> int:
    """Vérifie la validité d'un token JWT et extrait l'identifiant de l'utilisateur."""
    # Préparation de l'exception pour les erreurs d'authentification
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credentials invalides",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id_str: str = payload.get("sub")
        if user_id_str is None:
            raise credentials_exception

        user_id = int(user_id_str)
        user = get_user_by_id(user_id)

        if user is None:
            raise credentials_exception
        return user_id

    except (JWTError, ValueError):
        raise credentials_exception
