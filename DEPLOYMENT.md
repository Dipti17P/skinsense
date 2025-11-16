# 🚀 SkinSense Deployment Guide

## 📋 Table of Contents
1. [Local Development Setup](#local-development-setup)
2. [Environment Variables](#environment-variables)
3. [Database Setup](#database-setup)
4. [Deploying to Production](#deploying-to-production)
5. [Heroku Deployment](#heroku-deployment)
6. [AWS Deployment](#aws-deployment)

---

## 🏠 Local Development Setup

### Prerequisites
- Python 3.8+
- PostgreSQL 12+
- pip
- virtualenv

### Quick Start

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/skinsense.git
cd skinsense

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment variables
copy .env.example .env
# Edit .env with your actual values

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Populate database
python manage.py populate_quiz
python manage.py populate_products
python manage.py add_flipkart_links
python manage.py map_product_images

# Run development server
python manage.py runserver
```

Visit: http://127.0.0.1:8000/

---

## 🔐 Environment Variables

### Create .env file

Copy `.env.example` to `.env` and update with your values:

```env
# Required Settings
SECRET_KEY=your-very-long-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=skinsense_db
DB_USER=skinsense_user
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432
```

### Generate SECRET_KEY

```python
# Run in Python shell
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

---

## 🗄️ Database Setup

### PostgreSQL Installation

#### Windows:
1. Download from: https://www.postgresql.org/download/windows/
2. Run installer
3. Note the password you set for postgres user

#### Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

### Create Database

```sql
-- Connect to PostgreSQL
psql -U postgres

-- Create database and user
CREATE DATABASE skinsense_db;
CREATE USER skinsense_user WITH PASSWORD 'your_password';
ALTER ROLE skinsense_user SET client_encoding TO 'utf8';
ALTER ROLE skinsense_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE skinsense_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE skinsense_db TO skinsense_user;

-- Exit
\q
```

### Verify Connection

```bash
python manage.py dbshell
```

---

## 🌐 Deploying to Production

### Pre-Deployment Checklist

- [ ] Set `DEBUG = False`
- [ ] Update `ALLOWED_HOSTS`
- [ ] Configure static files
- [ ] Setup media files storage
- [ ] Use environment variables
- [ ] Enable HTTPS
- [ ] Setup logging
- [ ] Configure email backend
- [ ] Backup database

### Update settings.py for Production

```python
import os

# Security Settings
DEBUG = False
ALLOWED_HOSTS = ['your-domain.com', 'www.your-domain.com']
SECRET_KEY = os.environ.get('SECRET_KEY')

# HTTPS Settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Static Files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media Files (use cloud storage in production)
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
```

---

## 🔷 Heroku Deployment

### Prerequisites
- Heroku account: https://signup.heroku.com/
- Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli

### Step 1: Install Additional Packages

```bash
pip install gunicorn whitenoise dj-database-url psycopg2-binary
pip freeze > requirements.txt
```

### Step 2: Create Procfile

```procfile
web: gunicorn skinsense.wsgi --log-file -
```

### Step 3: Update settings.py

Add at the top:
```python
import dj_database_url
```

Update DATABASES:
```python
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL')
    )
}
```

Add WhiteNoise to MIDDLEWARE:
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this
    # ... rest of middleware
]
```

### Step 4: Create runtime.txt

```
python-3.11.0
```

### Step 5: Deploy to Heroku

```bash
# Login to Heroku
heroku login

# Create Heroku app
heroku create skinsense-app

# Set environment variables
heroku config:set SECRET_KEY="your-secret-key"
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS="skinsense-app.herokuapp.com"

# Add PostgreSQL addon
heroku addons:create heroku-postgresql:hobby-dev

# Push to Heroku
git push heroku main

# Run migrations
heroku run python manage.py migrate

# Create superuser
heroku run python manage.py createsuperuser

# Populate database
heroku run python manage.py populate_quiz
heroku run python manage.py populate_products

# Open app
heroku open
```

### Heroku Environment Variables

Set in Heroku dashboard or via CLI:
```bash
heroku config:set VARIABLE_NAME="value"
```

---

## ☁️ AWS Deployment (EC2 + RDS)

### Step 1: Launch EC2 Instance

1. Go to AWS Console → EC2
2. Launch Instance:
   - AMI: Ubuntu Server 22.04 LTS
   - Instance Type: t2.micro (free tier)
   - Security Group: Allow HTTP (80), HTTPS (443), SSH (22)
3. Create or select key pair
4. Launch instance

### Step 2: Connect to EC2

```bash
ssh -i your-key.pem ubuntu@your-ec2-public-ip
```

### Step 3: Setup Server

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3-pip python3-venv nginx postgresql-client -y

# Clone repository
git clone https://github.com/YOUR_USERNAME/skinsense.git
cd skinsense

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
pip install gunicorn
```

### Step 4: Setup RDS (PostgreSQL)

1. Go to AWS Console → RDS
2. Create Database:
   - Engine: PostgreSQL
   - Template: Free tier
   - DB instance identifier: skinsense-db
   - Master username: postgres
   - Master password: (set secure password)
3. Wait for database to be available
4. Note the endpoint URL

### Step 5: Configure Application

Create `.env`:
```env
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-ec2-public-ip,your-domain.com
DB_ENGINE=django.db.backends.postgresql
DB_NAME=skinsense_db
DB_USER=postgres
DB_PASSWORD=your-rds-password
DB_HOST=your-rds-endpoint.amazonaws.com
DB_PORT=5432
```

Run migrations:
```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
python manage.py populate_quiz
python manage.py populate_products
```

### Step 6: Setup Gunicorn

Create `/etc/systemd/system/gunicorn.service`:
```ini
[Unit]
Description=gunicorn daemon for SkinSense
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/skinsense
ExecStart=/home/ubuntu/skinsense/venv/bin/gunicorn \
    --workers 3 \
    --bind unix:/home/ubuntu/skinsense/skinsense.sock \
    skinsense.wsgi:application

[Install]
WantedBy=multi-user.target
```

Start Gunicorn:
```bash
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
```

### Step 7: Configure Nginx

Create `/etc/nginx/sites-available/skinsense`:
```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /home/ubuntu/skinsense;
    }
    
    location /media/ {
        root /home/ubuntu/skinsense;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/skinsense/skinsense.sock;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/skinsense /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

### Step 8: Setup SSL (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

---

## 🔄 Continuous Deployment

### GitHub Actions

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Deploy to Server
      uses: appleboy/ssh-action@master
      with:
        host: ${{ secrets.HOST }}
        username: ${{ secrets.USERNAME }}
        key: ${{ secrets.SSH_KEY }}
        script: |
          cd /home/ubuntu/skinsense
          git pull origin main
          source venv/bin/activate
          pip install -r requirements.txt
          python manage.py migrate
          python manage.py collectstatic --noinput
          sudo systemctl restart gunicorn
          sudo systemctl restart nginx
```

---

## 📊 Monitoring & Maintenance

### Setup Logging

```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'django-errors.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
```

### Database Backups

```bash
# Backup
pg_dump -U skinsense_user skinsense_db > backup_$(date +%Y%m%d).sql

# Restore
psql -U skinsense_user skinsense_db < backup_20250110.sql
```

### Automated Backups (Cron)

```bash
# Edit crontab
crontab -e

# Add daily backup at 2 AM
0 2 * * * pg_dump -U skinsense_user skinsense_db > /home/ubuntu/backups/backup_$(date +\%Y\%m\%d).sql
```

---

## 🐛 Troubleshooting

### Static Files Not Loading
```bash
python manage.py collectstatic --clear
python manage.py collectstatic --noinput
```

### Database Connection Error
- Check DATABASE_URL in environment variables
- Verify PostgreSQL is running
- Check firewall rules

### 502 Bad Gateway
```bash
sudo systemctl status gunicorn
sudo systemctl restart gunicorn
sudo systemctl restart nginx
```

---

## 📚 Additional Resources

- Django Deployment: https://docs.djangoproject.com/en/4.2/howto/deployment/
- Heroku Django: https://devcenter.heroku.com/articles/django-app-configuration
- AWS EC2: https://docs.aws.amazon.com/ec2/
- Digital Ocean Tutorials: https://www.digitalocean.com/community/tags/django

---

**Your SkinSense application is now ready for deployment! 🚀**
