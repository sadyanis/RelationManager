from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
import requests

# === Configuration Keycloak ===
KEYCLOAK_SERVER_URL = "http://localhost:8080"
REALM = "myrealm"  
CLIENT_ID = "fastapi-client"  
ALGORITHM = "RS256"

# === Initialisation du OAuth2PasswordBearer ===
# Cela récupère automatiquement le token dans le header Authorization
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{KEYCLOAK_SERVER_URL}/realms/{REALM}/protocol/openid-connect/token")

# === Charger la clé publique de Keycloak ===
def get_public_key():
    url = f"{KEYCLOAK_SERVER_URL}/realms/{REALM}/protocol/openid-connect/certs"
    response = requests.get(url)
    response.raise_for_status()
    jwks = response.json()
    return jwks['keys'][0]  # On prend la première clé (Keycloak les rotate rarement)

# On pré-charge la clé pour ne pas la re-télécharger à chaque requête
public_key = get_public_key()

# === Fonction pour vérifier le token ===
async def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(
            token,
            public_key,
            algorithms=[ALGORITHM],
            audience= "account",  # Audience du token, à adapter selon votre configuration
            issuer=f"{KEYCLOAK_SERVER_URL}/realms/{REALM}"
        )
        return payload  # On peut retourner le payload entier

    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token invalide : {e}"
        )

# === Optionnel : Fonction pour vérifier qu'un utilisateur a un rôle spécifique ===
def require_role(required_role: str):
    async def role_checker(token_data=Depends(verify_token)):
        roles = token_data.get("realm_access", {}).get("roles", [])
        if required_role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Accès interdit : rôle insuffisant"
            )
        return token_data
    return role_checker
