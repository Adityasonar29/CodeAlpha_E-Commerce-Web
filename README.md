# E-Commerce Store

A Django-based e-commerce web application with user authentication and admin dashboard.

## Features

- **Product Catalog**: Browse products with categories and brands
- **Shopping Cart**: Add/remove items, view cart details
- **User Authentication**: Registration, login (email or username), password reset
- **Checkout**: Place orders with total price calculation
- **User Dashboard**: View order history
- **Admin Dashboard**: Manage users and products

## Project Structure

```
e-commerce_store/
├── e_coomerce_site/          # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── store/                     # Main e-commerce app
│   ├── models.py             # Product, Order, OrderItem models
│   ├── views.py              # Application views
│   ├── urls.py               # App routes
│   ├── forms.py              # User forms
│   ├── cart.py               # Shopping cart logic
│   ├── backends.py           # Email/username authentication backend
│   └── templates/store/      # HTML templates
├── eccomerce_dataset/         # Product data
│   └── data.csv
└── manage.py                 # Django management script
```

## Setup

1. Install dependencies:

```bash
pip install django markdown
```

2. Run migrations:

```bash
python manage.py migrate
```

3. Create a superuser (optional, for admin access):

```bash
python manage.py createsuperuser
```

4. Start the development server:

```bash
python manage.py runserver
```

The site will be available at `http://localhost:8000`

## Models

- **Product**: name, description, price, stock, image_url, featured, brand, category
- **Order**: user, created_at, total_price
- **OrderItem**: order, product, quantity, price
