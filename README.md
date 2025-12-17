 # <img src="https://github.com/elias-utf8/api-poleinfo/blob/main/assets/logo.png" alt="logo" width="250"/>

 Cette API développée en Python est un composant d'un projet académique de fin de seconde année de BTS. 
> [!IMPORTANT]
>
> **Status**: Ceci n'est qu'une partie du projet, pour consulter ce dernier en entier vous pouvez consulter le rapport [ici](https://raw.githubusercontent.com/elias-utf8/api-poleinfo/main/assets/BTS_CIEL_2025_E6_LP2I_GauthierElias.pdf).
>

> Page d'accueil
![image](https://raw.githubusercontent.com/elias-utf8/api-poleinfo/main/assets/accueil.png)

> Page de login
![image](https://raw.githubusercontent.com/elias-utf8/api-poleinfo/main/assets/login.png)

> Tableau de bord
![image](https://raw.githubusercontent.com/elias-utf8/api-poleinfo/main/assets/dashboard.png)

## Déploiement local
Vous ne pourrez pas tester les endpoints, car cela nécessitera une configuration complète de MariaDB. Cependant, suivez les instructions ci-dessous pour explorer l’architecture de l’API en local.

 ```bash
git clone https://github.com/elias-utf8/api-poleinfo.git
cd api-poleinfo
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```
