

# 🛒 **EROLS Backend – API Django REST**

**Plateforme : EROLS EasyBuy – Le marché chinois à votre porte**
**Entreprise : VisionTech**

---

## ⭐ **1. Présentation du projet**

**EROLS Backend** est l’API officielle de la plateforme e-commerce **EROLS EasyBuy**, qui connecte les consommateurs et revendeurs camerounais au marché chinois.
Elle gère :

* Les utilisateurs
* Les produits chinois & locaux
* Les commandes
* La livraison & le transit
* La marketplace locale
* Les notifications
* Le service client

Ce backend est conçu pour être **scalable, sécurisé, propre et facilement contributif**.

---

# 📁 **2. Structure du projet**

```
erols_backend/
├── config/                  # Paramètres Django (settings, urls, wsgi, asgi)
├── apps/                    # Applications principales
│   ├── users/               # Auth, JWT, profils, permissions
│   ├── products/            # Produits chinois & locaux, catégories
│   ├── orders/              # Commandes, transactions, paniers
│   ├── delivery/            # Transit, tracking, points relais, tarifs
│   ├── marketplace/         # Boutiques fournisseurs locaux
│   └── notifications/       # Emails, SMS, push notifications, WebSockets
├── core/                    # Outils communs (utils, mixins, modèles abstraits)
├── media/                   # Uploads (images produits, documents)
├── manage.py
└── Dockerfile / config files
```

---

# 🧰 **3. Technologies utilisées**

### **Backend**

* Django
* Django REST Framework
* Django Filter
* SimpleJWT
* Celery + Redis (tâches asynchrones)
* PostgreSQL

### **DevOps**

* Docker
* Render 
* GitHub Actions 

---

# 🚀 **4. Installation & exécution (mode développement)**

### **1️⃣ Cloner le projet**

```bash
git clone https://github.com/visiontech/erols_backend.git
cd erols_backend
```

### **2️⃣ Créer l’environnement virtuel**

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### **3️⃣ Installer les dépendances**

```bash
pip install -r requirements.txt
```

### **4️⃣ Configurer les variables d’environnement**

Créer un fichier `.env` à la racine :

```
DEBUG=True
SECRET_KEY=change_me
DATABASE_URL=postgres://user:password@localhost:5432/erols
REDIS_URL=redis://localhost:6379/0
ALLOWED_HOSTS=*
```

### **5️⃣ Appliquer les migrations**

```bash
python manage.py migrate
```

### **6️⃣ Lancer le serveur**

```bash
python manage.py runserver
```

---

# 🐳 **5. Exécution avec Docker**

### **Construire l’image**

```bash
docker build -t erols-backend .
```

### **Lancer le conteneur**

```bash
docker run -p 8000:8000 erols-backend
```

---

# 📡 **6. Documentation API**

La documentation interactive est disponible après lancement :

* Swagger UI → `/api/docs/`
* Redoc → `/api/redoc/`
* Schema OpenAPI → `/api/schema/`

---

# 👥 **7. Règles pour les contributeurs**

### 🔹 1. Créer une branche par fonctionnalité

```
feature/nom_fonction
bugfix/nom_bug
hotfix/nom_fix
```

### 🔹 2. Respecter la structure des apps

Chaque module doit rester isolé et cohérent.

### 🔹 3. PEP8 + conventions Django

Utiliser `flake8` ou `black` (si configuré).

### 🔹 4. Ajouter tests et documentation pour chaque nouvelle API

### 🔹 5. Commit messages clairs

Exemples :

```
feat(users): add jwt authentication
fix(orders): correct total calculation bug
```

---

# 📦 **8. Fonctionnalités principales (MVP)**

### 🛍️ **Produits**

* Produits chinois importés
* Produits fournisseurs locaux
* Catégories & variantes

### 🧑‍💻 **Utilisateurs**

* Inscription / connexion via JWT
* Profil
* Rôles : client, vendeur, admin

### 🛒 **Commandes**

* Panier
* Commande
* Réservation sans paiement
* Suivi du statut

### 🚚 **Livraison**

* Points relais
* Livraison domicile
* Suivi en temps réel

### 🏪 **Marketplace**

* Création de boutique
* Produits fournisseurs
* Commissions transparentes

### 🔔 **Notifications**

* Email
* WhatsApp (intégration future)
* Notifications système

---

# 🌐 **9. Déploiement (Docker + Render)**

Le backend peut être déployé via :

* **Render (Dockerfile)**
* **Railway**
* **OVH Cloud**
* **VPS Ubuntu + Docker Compose**

Un fichier `render.yaml` peut automatiser le déploiement.

---

# 🙌 **10. Contributeurs**

Merci à tous ceux qui participent à l’évolution de **EROLS EasyBuy**.
Chaque contribution apporte une pierre au pont numérique entre le Cameroun et la Chine.

---

# 📞 **Contact**

📧 [visiontech.ft@gmail.com](mailto:support@visiontech.cm)
🌍 [www.erols.cm](http://www.erols.cm) (à venir)

