"""
Routes de gestion des utilisateurs (création, consultation, suppression).

Auteur: Elias GAUTHIER
"""

from fastapi import APIRouter, Depends, HTTPException, status

from core.security import verify_admin
from db.requests.user import create_user, delete_user_by_login, get_all_users, get_user_by_login
from models.schemas import UserCreate, UserDelete, UserResponse

# Définition du router avec le tag pour la documentation Swagger
router = APIRouter(tags=["utilisateurs"])


@router.post(
    "/",
    response_model=dict,
    responses={
        400: {"description": "Un utilisateur avec ce login existe déjà"},
    },
)
def add_user(user: UserCreate, admin_id: int = Depends(verify_admin)):
    """
    Ajoute un nouvel utilisateur dans le système.

    Cette route est protégée et nécessite des privilèges administrateur.
    Elle effectue une vérification pour s'assurer que le login n'existe pas déjà.

    Args:
        user (UserCreate): Données du nouvel utilisateur
        admin_id (int): ID de l'administrateur authentifié

    Returns:
        dict: Message de confirmation avec l'identifiant de l'utilisateur créé
    """
    existing_user = get_user_by_login(user.login)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Un utilisateur avec ce login existe déjà")

    user_id = create_user(login=user.login, password=user.password, type=user.type, nom=user.nom, prenom=user.prenom)

    return {"message": "Utilisateur créé avec succès", "id": user_id}


@router.delete(
    "/",
    response_model=dict,
    responses={
        404: {"description": "Utilisateur non trouvé"},
        500: {"description": "Erreur lors de la suppression de l'utilisateur"},
    },
)
def delete_users(user: UserDelete, user_id: int = Depends(verify_admin)):
    """
    Supprime un utilisateur existant.

    Cette opération nécessite des droits administrateur.

    Args:
        user (UserDelete): Données de l'utilisateur à supprimer
        user_id (int): ID de l'administrateur authentifié

    Returns:
        dict: Message de confirmation de la suppression
    """
    existing_user = get_user_by_login(user.login)

    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Utilisateur non trouvé")

    result = delete_user_by_login(user.login)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erreur lors de la suppression de l'utilisateur"
        )

    return {"message": f"Utilisateur avec login '{user.login}' supprimé avec succès"}


@router.get(
    "/",
    response_model=list[UserResponse],
    responses={
        404: {"description": "Aucun utilisateur trouvé"},
    },
)
def get_users():
    """
    Récupère la liste de tous les utilisateurs.

    Returns:
        List[UserResponse]: Liste des utilisateurs enregistrés
    """
    users = get_all_users()

    if len(users) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucun utilisateur trouvé")

    return users
