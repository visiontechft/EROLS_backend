

```bash
# Créer le superuser
docker exec -it erols_backend-backend-1 python manage.py createsuperuser

# Ou avec docker-compose
docker-compose -f docker-compose.dev.yml exec backend python manage.py createsuperuser
```


```bash
# Migrations
docker exec -it erols_backend-backend-1 python manage.py makemigrations
docker exec -it erols_backend-backend-1 python manage.py migrate

# Accéder au shell Django
docker exec -it erols_backend-backend-1 python manage.py shell

# Voir les logs du backend
docker logs erols_backend-backend-1 -f

# Arrêter tous les conteneurs
docker-compose -f docker-compose.dev.yml down

# Reconstruire les images 
docker-compose -f docker-compose.dev.yml build

#relancer les images

docker-compose -f docker-compose.dev.yml up -d


# Redémarrer un conteneur spécifique
docker restart erols_backend-backend-1
```
# copie du fichier dans docker
docker cp seed_products.py erols_backend-backend-1:/app/

# execution
docker exec -it erols_backend-backend-1 python seed_products.py
