# Projet d'authentification avec OTP

- Tous les exercices sont présents, ne pas se fier au nom du dossier 'Exercice_1'
- Ce projet Django met en œuvre une solution d'authentification avec un système de validation par code OTP (One Time Password). Les utilisateurs doivent s'authentifier avec un nom d'utilisateur et un mot de passe. Ensuite, un code OTP est généré et envoyé à leur adresse e-mail. Une fois l'OTP validé, l'utilisateur obtient des jetons d'authentification JWT (JSON Web Tokens).

## Prérequis

- Python 3.12
- Django
- Django REST Framework
- smtplib (inclus avec Python pour l'envoi d'emails)
- `djangorestframework-simplejwt` pour la gestion des JWT

## Installation

1. **Cloner le dépôt**

   ```bash
   git clone <url_du_depot>
   cd <nom_du_projet>
   ```
  
2. **Virtual Environment**

   ```bash
    python3 -m venv venv
    source venv/bin/activate
   ```
3. **Install dependencies**

   ```bash
    pip install -r requirements.txt
   ```   
   
4. **Migration**

   ```bash
    python manage.py migrate
   ```      

5. **Create superuser**

   ```bash
    python manage.py createsuperuser
   ```        

6. **Create .env**

   ```bash
    touch .env
    email=""
    password=""
   ```  
   
7. **Launch server**

   ```bash
    python manage.py runserver
   ```       
   
## Known problems 
   
- SMTP connection problem: If ConnectionRefusedError occurs, check SMTP settings and network firewalls.
- SMTP authentication error (535): Make sure that basic authentication is not disabled in your e-mail provider.
   