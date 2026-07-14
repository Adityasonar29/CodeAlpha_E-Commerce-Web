from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
   path('', views.home, name='home'),
   path('products/', views.product_list, name='product_list'),
   path('product/<int:pk>/', views.product_detail, name='product_detail'),
   path('cart/', views.cart_detail, name='cart_detail'),
   path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),

   # Auth Routes
   path('register/', views.register, name='register'),
   path('login/', views.CustomLoginView.as_view(), name='login'),
   path('password-reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
   path('logout/', auth_views.LogoutView.as_view(next_page='product_list'), name='logout'),

   path('checkout/', views.checkout, name='checkout'),

   path('dashboard/', views.user_dashboard, name='user_dashboard'),
   path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
   path('admin-users/', views.admin_users, name='admin_users'),
   path('admin-users/<int:user_id>/', views.admin_user_detail, name='admin_user_detail'),
   path('admin-users/<int:user_id>/edit/', views.admin_user_update, name='admin_user_update'),
   path('admin-users/<int:user_id>/delete/', views.admin_user_delete, name='admin_user_delete'),
   path('admin-products/', views.admin_products, name='admin_products'),
   path('admin-products/<int:product_id>/', views.admin_product_detail, name='admin_product_detail'),
   path('admin-products/<int:product_id>/edit/', views.admin_product_update, name='admin_product_update'),
   path('admin-products/<int:product_id>/delete/', views.admin_product_delete, name='admin_product_delete'),
]
