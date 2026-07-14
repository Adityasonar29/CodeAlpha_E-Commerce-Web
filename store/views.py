from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomRegistrationForm, AdminUserForm, ProductForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, PasswordResetView
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Sum, Count, F
from .models import Product, Order, OrderItem
from .cart import Cart
import markdown


class CustomLoginView(LoginView):
    template_name = 'store/login.html'

    def form_valid(self, form):
        remember_me = self.request.POST.get('remember_me') == 'on'
        if remember_me:
            self.request.session.set_expiry(60 * 60 * 24 * 7)
        else:
            self.request.session.set_expiry(0)
        return super().form_valid(form)

def home(request):
    featured_products = Product.objects.filter(featured=True, stock__gt=0).order_by('-id')
    total_products = Product.objects.filter(stock__gt=0).count()
    featured_count = featured_products.count()
    return render(request, 'store/home.html', {
        'featured_products': featured_products,
        'total_products': total_products,
        'featured_count': featured_count,
    })


class CustomPasswordResetView(PasswordResetView):
    template_name = 'store/password_reset.html'
    email_template_name = 'store/password_reset_email.html'
    success_url = '/login/'


@login_required(login_url='login')
def admin_dashboard(request):
    if not request.user.is_staff and not request.user.is_superuser:
        messages.error(request, 'You do not have access to the admin dashboard.')
        return redirect('product_list')

    total_users = User.objects.count()
    total_orders = Order.objects.count()
    total_products = Product.objects.count()
    featured_count = Product.objects.filter(featured=True).count()
    normal_products_count = total_products - featured_count
    out_of_stock_count = Product.objects.filter(stock=0).count()
    low_stock_products = Product.objects.filter(stock__gt=0, stock__lte=3).order_by('stock')
    out_of_stock_products = Product.objects.filter(stock=0).order_by('name')
    latest_orders = Order.objects.select_related('user').order_by('-created_at')[:5]

    product_analytics = []
    for product in Product.objects.all().order_by('-id'):
        sold_qty = OrderItem.objects.filter(product=product).aggregate(total=Sum('quantity'))['total'] or 0
        order_count = OrderItem.objects.filter(product=product).count()
        product_analytics.append({
            'product': product,
            'quantity_sold': sold_qty,
            'order_count': order_count,
        })
    product_analytics.sort(key=lambda item: item['quantity_sold'], reverse=True)

    total_revenue = Order.objects.aggregate(total=Sum('total_price'))['total'] or 0

    return render(request, 'store/dashboard.html', {
        'total_users': total_users,
        'total_orders': total_orders,
        'total_products': total_products,
        'featured_count': featured_count,
        'normal_products_count': normal_products_count,
        'out_of_stock_count': out_of_stock_count,
        'low_stock_products': low_stock_products,
        'out_of_stock_products': out_of_stock_products,
        'latest_orders': latest_orders,
        'product_analytics': product_analytics,
        'total_revenue': total_revenue,
        'orders': latest_orders,
    })


@login_required(login_url='login')
def admin_users(request):
    if not request.user.is_staff and not request.user.is_superuser:
        messages.error(request, 'You do not have access to this area.')
        return redirect('product_list')

    users = User.objects.order_by('-id')
    if request.method == 'POST':
        form = AdminUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_staff = True
            user.save()
            messages.success(request, f'User {user.username} created successfully.')
            return redirect('admin_users')
    else:
        form = AdminUserForm()

    return render(request, 'store/admin_users.html', {
        'users': users,
        'form': form,
    })


@login_required(login_url='login')
def admin_products(request):
    if not request.user.is_staff and not request.user.is_superuser:
        messages.error(request, 'You do not have access to this area.')
        return redirect('product_list')

    products = Product.objects.order_by('-id')
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product created successfully.')
            return redirect('admin_products')
    else:
        form = ProductForm()

    return render(request, 'store/admin_products.html', {
        'products': products,
        'form': form,
    })


@login_required(login_url='login')
def admin_product_detail(request, product_id):
    if not request.user.is_staff and not request.user.is_superuser:
        messages.error(request, 'You do not have access to this area.')
        return redirect('product_list')

    product = get_object_or_404(Product, id=product_id)
    return render(request, 'store/admin_product_detail.html', {
        'product': product,
    })


@login_required(login_url='login')
def admin_product_update(request, product_id):
    if not request.user.is_staff and not request.user.is_superuser:
        messages.error(request, 'You do not have access to this area.')
        return redirect('product_list')

    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully.')
            return redirect('admin_product_detail', product_id=product.id)
    else:
        form = ProductForm(instance=product)

    return render(request, 'store/admin_product_update.html', {
        'product': product,
        'form': form,
    })


@login_required(login_url='login')
def admin_product_delete(request, product_id):
    if not request.user.is_staff and not request.user.is_superuser:
        messages.error(request, 'You do not have access to this area.')
        return redirect('product_list')

    product = get_object_or_404(Product, id=product_id)
    product.delete()
    messages.success(request, 'Product deleted successfully.')
    return redirect('admin_products')


@login_required(login_url='login')
def admin_user_detail(request, user_id):
    if not request.user.is_staff and not request.user.is_superuser:
        messages.error(request, 'You do not have access to this area.')
        return redirect('product_list')

    user = get_object_or_404(User, id=user_id)
    user_orders = Order.objects.filter(user=user).order_by('-created_at')
    return render(request, 'store/admin_user_detail.html', {
        'selected_user': user,
        'user_orders': user_orders,
    })


@login_required(login_url='login')
def admin_user_update(request, user_id):
    if not request.user.is_staff and not request.user.is_superuser:
        messages.error(request, 'You do not have access to this area.')
        return redirect('product_list')

    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.save(update_fields=['first_name', 'last_name', 'email'])
        messages.success(request, f'Updated {user.username} successfully.')
        return redirect('admin_user_detail', user_id=user.id)

    return render(request, 'store/admin_user_update.html', {'selected_user': user})


@login_required(login_url='login')
def admin_user_delete(request, user_id):
    if not request.user.is_staff and not request.user.is_superuser:
        messages.error(request, 'You do not have access to this area.')
        return redirect('product_list')

    user = get_object_or_404(User, id=user_id)
    if request.user.id == user.id:
        messages.error(request, 'You cannot delete your own account.')
        return redirect('admin_users')

    username = user.username
    user.delete()
    messages.success(request, f'Deleted user {username}.')
    return redirect('admin_users')


def product_list(request):
    sort = request.GET.get('sort', 'latest')
    products = Product.objects.filter(stock__gt=0)
    out_of_stock_products = Product.objects.filter(stock=0)
    if sort == 'price_low':
        products = products.order_by('price')
        out_of_stock_products = out_of_stock_products.order_by('price')
    elif sort == 'price_high':
        products = products.order_by('-price')
        out_of_stock_products = out_of_stock_products.order_by('-price')
    else:
        products = products.order_by('-id')
        out_of_stock_products = out_of_stock_products.order_by('-id')

    featured_count = Product.objects.filter(featured=True, stock__gt=0).count()
    return render(request, 'store/product_list.html', {
        'products': products,
        'out_of_stock_products': out_of_stock_products,
        'sort': sort,
        'featured_count': featured_count,
    })


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/product_detail.html', {'product': product})

# View to process adding an item to the session cart
def add_to_cart(request, product_id):
    # Check if user is logged in manually so we can send a custom message
    if not request.user.is_authenticated:
        messages.warning(request, "You need to log in to add items to your cart and place an order.")
        return redirect('login')

    product = get_object_or_404(Product, id=product_id)
    try:
        quantity = int(request.POST.get('quantity', 1))
    except (TypeError, ValueError):
        quantity = 1

    if quantity < 1:
        quantity = 1

    cart = Cart(request)
    current_quantity = cart.cart.get(str(product_id), {}).get('quantity', 0)
    if current_quantity + quantity > product.stock:
        messages.error(request, f'Sorry, only {product.stock} "{product.name}" available in stock.')
        return redirect(request.META.get('HTTP_REFERER', 'product_list'))

    cart.add(product_id, quantity=quantity)
    
    messages.success(request, f'"{product.name}" has been added to your cart.')
    return redirect(request.META.get('HTTP_REFERER', 'product_list'))

# View to render what is inside the cart
@login_required(login_url='login') # <-- Protect the cart page too
def cart_detail(request):
    cart = Cart(request)
    products_in_cart = []
    total_price = 0
    
    # Loop through session data to gather database objects
    for item_id, item_data in cart.cart.items():
        product = get_object_or_404(Product, id=item_id)
        subtotal = product.price * item_data['quantity']
        total_price += subtotal
        products_in_cart.append({
            'product': product,
            'quantity': item_data['quantity'],
            'subtotal': subtotal
        })
        
    return render(request, 'store/cart_detail.html', {
        'cart_items': products_in_cart,
        'total_price': total_price
    })

@login_required(login_url='login')
def checkout(request):
    cart = Cart(request)
    if not cart.cart:
        return redirect('product_list') # Can't checkout with an empty cart
        
    total_price = 0
    order_items_to_create = []

    # Validate stock and prepare order data inside a transaction
    with transaction.atomic():
        for item_id, item_data in cart.cart.items():
            product = Product.objects.select_for_update().get(id=item_id)
            quantity = item_data['quantity']
            if quantity > product.stock:
                messages.error(request, f'Not enough stock for "{product.name}". Only {product.stock} available.')
                return redirect('cart_detail')

            subtotal = product.price * quantity
            total_price += subtotal
            order_items_to_create.append((product, quantity, product.price))

        # Save Order
        order = Order.objects.create(user=request.user, total_price=total_price)

        # Save individual ordered items and decrement inventory
        for product, qty, price in order_items_to_create:
            OrderItem.objects.create(order=order, product=product, quantity=qty, price=price)
            product.stock = max(product.stock - qty, 0)
            product.save(update_fields=['stock'])

    # Clear the cart from sessions
    request.session['cart'] = {}
    request.session.modified = True
    
    return render(request, 'store/order_success.html', {'order': order})

@login_required(login_url='login')
def user_dashboard(request):
    user_orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/user_dashboard.html', {
        'orders': user_orders,
        'total_orders': user_orders.count(),
    })
    
def register(request):
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Explicitly specify the backend path here to prevent lookup errors
            login(request, user, backend='store.backends.EmailOrUsernameBackend')
            return redirect('product_list')
    else:
        form = CustomRegistrationForm()
    return render(request, 'store/register.html', {'form': form})
