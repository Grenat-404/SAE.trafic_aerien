# Lancement Django
Pour le lancement du projet, il faut le récupérer sur githhub.io sur le lien suivant :
https://github.com/Grenat-404/SAE.trafic_aerien
Une fois le projet ouvert dans un environnement de développement, il faut faire une suite de
commandes pour activer le projet en local.

Déplacement dans le bon dossier
cd gestion_traffic
Créer l'environnement virtuel
python3 -m venv venv
Sous Linux/macOS
python3 -m venv venv
source venv/bin/activate
Sous Windows
python -m venv venv
venv\Scripts\Activate.ps1

Une fois que (venv) est affiché à coté du chemin, il est temps d’activer les différentes dépendances :
pip install django #code
pip install reportLab #pdf
pip install mysqlclient #base de données
pip install Pillow #images

Après il est temps de relier la base de données grâces à la migration de celles-ci
Appliquer les migrations
python manage.py makemigrations
python manage.py migrate

Et pour finir, on lance le serveur django :
python manage.py runserver
Et le site sera accessible depuis l’adresse suivante : http://127.0.0.1:8000

# Sur la VM1 (Base de Données) :
• Vérifier si mariadb est en fonctionnement : sudo systemctl status mariadb (si pas actif faire
sudo systemctl start mariadb)
• Pour accéder à mariadb faire : sudo mariadb
• On peut voir les bases de données présentes en faisant : SHOW DATABASES ;
• Pour voir les tables de notre base de donnée on doit d’abord aller sur la bonne base de
donéee : USE trafic_aerien ;
• Ensuite pour lister les tables on fait : SHOW TABLES ;
• Pour afficher le contenu d’une table : SELECT * FROM nomdelatable ;

# Sur la VM2 (Serveur Web) :
1. Activer l’environnement virtuel Python
• Pour accéder aux fichiers du projet :
cd /Votre/Chemin/SAE23_trafic_aerien/gestion_traffic/
• Puis pour lancer l’environnement virtuel : source /home/debian/venv/bin/activate
• Installer les dépendances : pip install django, Pillow, mysqlclient, reportLab
• Vérifier dans settings.py la route préciser pour le fichier css
• Lancer gunicorn avec : /Votre/Chemin/venv/bin/gunicorn
gestion_traffic.wsgi:application --bind 127.0.0.1:8000
2. Vérifier la configuration Nginx :
• Faire : sudo nano /etc/nginx/sites-available/gestion_traffic
• Exemple de configuration :
server {
listen 80;
server_name 192.168.X.X; # IP locale de la VM2 ou nom de domaine
location / {
proxy_pass http://127.0.0.1:8000;
proxy_set_header Host $host;
proxy_set_header X-Real-IP $remote_addr;
}
location /static/ {
alias /home/debian/Documents/SAE23_trafic_aerien/staticfiles/;
}
}
• Ne pas oublier de créer le lien symbolique : sudo ln -s /etc/nginx/sites-
available/gestion_traffic /etc/nginx/sites-enabled/
3. Redémarrer Nginx :
• sudo systemctl restart nginx
4. Modifier les ALLOWED_HOSTS dans settings.py :
• ALLOWED_HOSTS = ['192.168.X.X', 'localhost'] # ajouter IP de la VM
Matthieu D., Tom B., Huseyin O. 3
5. Accéder au site :
Taper l’addresse IP de la VM dans un navigateur internet
