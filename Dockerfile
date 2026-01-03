FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Installation des dépendances système
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Installation des dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code source
COPY . .

# Copie et rend exécutable le script de démarrage
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

EXPOSE 8000

# Utilise le script de démarrage
CMD ["/app/start.sh"]