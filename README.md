# 🧴 SkinSense - Smart Skin Product Recommender

![SkinSense Banner](https://images.unsplash.com/photo-1596755389378-c31d21fd1273?w=1200&q=80)

## 📋 Overview

**SkinSense** is an intelligent skincare recommendation system that helps users discover the perfect skincare products based on their unique skin type and concerns. Built with Django and featuring a beautiful, modern UI with smooth animations.

## ✨ Features

- 🎯 **Personalized Quiz**: Interactive 5-question quiz to determine your skin type
- 🛍️ **Product Catalog**: Browse 25+ curated skincare products from top brands
- 🔍 **Smart Filtering**: Filter products by skin type (Dry, Oily, Combination, Sensitive, Normal)
- 🎨 **Beautiful UI**: Modern gradient design with smooth animations and transitions
- 📱 **Responsive Design**: Works perfectly on desktop and mobile devices
- 🔐 **User Authentication**: Secure login and signup system
- 📊 **Dashboard**: Personalized user dashboard with stats and recommendations
- 🛒 **Direct Purchase Links**: Quick access to Flipkart for product purchases

## 🚀 Technology Stack

- **Backend**: Django 4.2
- **Database**: PostgreSQL
- **Frontend**: Bootstrap 5.3.3, Tailwind CSS
- **Animations**: Animate.css, Custom CSS animations
- **Icons & Fonts**: Google Fonts (Poppins)
- **Images**: Pillow for image handling

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- PostgreSQL 12 or higher
- pip (Python package manager)

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd skinsense
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Database

1. Create a PostgreSQL database:

```sql
CREATE DATABASE skinsense_db;
CREATE USER skinsense_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE skinsense_db TO skinsense_user;
```

2. Update `skinsense/settings.py` with your database credentials:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'skinsense_db',
        'USER': 'skinsense_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Step 5: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Create Superuser

```bash
python manage.py createsuperuser
```

### Step 7: Populate Database

```bash
# Populate quiz questions
python manage.py populate_quiz

# Populate products
python manage.py populate_products

# Add Flipkart links to products
python manage.py add_flipkart_links

# Map product images
python manage.py map_product_images
```

### Step 8: Run Development Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to see the application!

## 📁 Project Structure

```
skinsense/
├── accounts/              # User authentication and index page
│   ├── views.py
│   ├── urls.py
│   └── models.py
├── products/              # Product catalog and management
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── management/
│       └── commands/
│           ├── populate_products.py
│           ├── add_flipkart_links.py
│           └── map_product_images.py
├── quiz/                  # Skin type quiz functionality
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── management/
│       └── commands/
│           └── populate_quiz.py
├── skinsense/             # Main project settings
│   ├── settings.py
│   ├── urls.py
│   └── views.py
├── templates/             # HTML templates
│   ├── accounts/
│   │   ├── index.html
│   │   ├── login.html
│   │   └── signup.html
│   ├── products/
│   │   └── product_list.html
│   ├── quiz/
│   │   ├── start_quiz.html
│   │   ├── question.html
│   │   └── result.html
│   ├── base.html
│   └── dashboard.html
├── media/                 # User uploaded files
│   └── product_images/    # Product screenshots
├── manage.py
├── requirements.txt
└── README.md
```


## 🌐 Routes

- `/` - Landing page
- `/accounts/login/` - User login
- `/accounts/signup/` - User registration
- `/dashboard/` - User dashboard
- `/quiz/start/` - Start skin type quiz
- `/quiz/question/<id>/` - Quiz questions
- `/quiz/result/` - Quiz results
- `/products/` - Product catalog
- `/admin/` - Django admin panel

## 👥 User Flow

1. **Landing Page** → View attractive hero section with features
2. **Sign Up/Login** → Create account or login
3. **Dashboard** → View personalized dashboard
4. **Take Quiz** → Answer 5 questions about skin
5. **Get Results** → Receive skin type determination
6. **Browse Products** → Filter by skin type
7. **Purchase** → Click to buy on Flipkart

## 🎯 Features in Detail

### Quiz System
- 5 carefully crafted questions
- Progress bar tracking
- Instant result calculation
- Skin type recommendations

### Product Catalog
- 25+ premium products
- Filter by 5 skin types
- Beautiful card design
- Direct Flipkart links
- Product images and descriptions

### Dashboard
- Welcome message with username
- Statistics cards (Users, Products, Questions)
- Quick action buttons
- Featured products carousel
- How It Works section
- Skin types exploration
- User testimonials

## 🔒 Security Features

- CSRF protection
- Password hashing
- SQL injection prevention
- XSS protection
- Secure session management

## 📱 Responsive Design

- Mobile-first approach
- Breakpoints for all devices
- Touch-friendly interface
- Optimized images

## 🚀 Performance

- GPU-accelerated animations
- Optimized image loading
- Lazy loading support
- Minimized CSS/JS
- Efficient database queries

## 👨‍💻 Author

**Dipti Patil**

## 🙏 Acknowledgments

- Bootstrap for responsive framework
- Tailwind CSS for utility classes
- Unsplash for beautiful images
- Animate.css for animation library
- Google Fonts for Poppins font
- Django community for excellent documentation



---

**Made with ❤️ by Dipti** | © 2025 SkinSense. All rights reserved.
