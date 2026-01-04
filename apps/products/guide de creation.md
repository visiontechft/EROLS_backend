# 3. Utilisation de la commande

## Créer la catégorie par défaut
```bash
python manage.py seed_products
````

## Créer une catégorie spécifique

```bash
python manage.py seed_products --category electronique
python manage.py seed_products --category mode
python manage.py seed_products --category maison
```

## Créer toutes les catégories

```bash
python manage.py seed_products --category toutes
```

## Supprimer et recréer toutes les catégories

```bash
python manage.py seed_products --category toutes --clear
```

# 4. Aide de la commande

```bash
python manage.py seed_products --help
python manage.py seed_cities
