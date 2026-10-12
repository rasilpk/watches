import random
import string
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q, Sum, Avg
from .models import Product, Order, OrderItem, Review, CATEGORY_CHOICES, ORDER_STATUS_CHOICES

def generate_tracking_number():
    random_digits = ''.join(random.choices(string.digits, k=8))
    return f"CLX-{random_digits}"

def home(request):
    query = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()
    brand = request.GET.get('brand', '').strip()
    sort = request.GET.get('sort', 'featured')
    min_price = request.GET.get('min_price', '').strip()
    max_price = request.GET.get('max_price', '').strip()
    
    products = Product.objects.all()

    if category:
        products = products.filter(category__iexact=category)
    
    if brand:
        products = products.filter(brand__iexact=brand)

    if min_price and min_price.isdigit():
        products = products.filter(price__gte=int(min_price))

    if max_price and max_price.isdigit():
        products = products.filter(price__lte=int(max_price))

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(brand__icontains=query) |
            Q(description__icontains=query) |
            Q(category__icontains=query)
        )

    # Sorting
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'newest':
        products = products.order_by('-created_at')
    elif sort == 'name':
        products = products.order_by('name')
    else:
        # Default featured
        products = products.order_by('-is_featured', '-created_at')

    # Available brands and categories
    all_brands = Product.objects.values_list('brand', flat=True).distinct().order_by('brand')
    categories = [c[0] for c in CATEGORY_CHOICES]

    context = {
        'products': products,
        'query': query,
        'selected_category': category,
        'selected_brand': brand,
        'selected_sort': sort,
        'min_price': min_price,
        'max_price': max_price,
        'categories': categories,
        'brands': all_brands,
        'total_count': products.count(),
    }
    return render(request, 'home.html', context)

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    related_products = Product.objects.filter(category=product.category).exclude(pk=pk)[:4]
    reviews = product.reviews.all().order_by('-created_at')
    
    review_count = reviews.count()
    if review_count > 0:
        avg_rating = round(sum(r.rating for r in reviews) / review_count, 1)
    else:
        avg_rating = 5.0

    return render(request, 'product_detail.html', {
        'product': product,
        'related_products': related_products,
        'reviews': reviews,
        'review_count': review_count,
        'avg_rating': avg_rating,
        'star_range': range(1, 6),
    })

def add_review(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        author = request.POST.get('author', '').strip()
        title = request.POST.get('title', '').strip()
        comment = request.POST.get('comment', '').strip()
        rating = int(request.POST.get('rating', 5))

        if author and comment:
            Review.objects.create(
                product=product,
                author=author,
                title=title,
                comment=comment,
                rating=min(max(rating, 1), 5),
                is_verified=True
            )
            messages.success(request, "Thank you! Your certified review has been posted.")
        else:
            messages.error(request, "Please provide your name and review remarks.")

    return redirect('product_detail', pk=pk)

def toggle_wishlist(request, pk):
    product = get_object_or_404(Product, pk=pk)
    wishlist = request.session.get('wishlist', [])
    if not isinstance(wishlist, list):
        wishlist = []

    if pk in wishlist:
        wishlist.remove(pk)
        messages.info(request, f'Removed "{product.name}" from your Wishlist.')
    else:
        wishlist.append(pk)
        messages.success(request, f'Saved "{product.name}" to your Wishlist.')

    request.session['wishlist'] = wishlist
    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or 'home'
    return redirect(next_url)

def wishlist_view(request):
    wishlist_ids = request.session.get('wishlist', [])
    if not isinstance(wishlist_ids, list):
        wishlist_ids = []

    products = Product.objects.filter(pk__in=wishlist_ids)
    return render(request, 'wishlist.html', {
        'products': products,
        'wishlist_count': products.count(),
    })

def track_order(request):
    order_query = request.GET.get('q', '').strip()
    order = None
    step_index = 0

    if order_query:
        if order_query.isdigit():
            order = Order.objects.filter(id=int(order_query)).first()
        elif order_query.upper().startswith('CLX-'):
            order = Order.objects.filter(tracking_number__iexact=order_query).first()
        else:
            order = Order.objects.filter(email__iexact=order_query).order_by('-created_at').first()

        if not order:
            messages.error(request, f'No order found matching "{order_query}". Please verify your Order ID or tracking code.')
        else:
            if order.status == 'Processing':
                step_index = 1
            elif order.status == 'Inspected & Dispatched':
                step_index = 2
            elif order.status == 'Delivered':
                step_index = 3
            else:
                step_index = 0

    return render(request, 'track_order.html', {
        'order': order,
        'order_query': order_query,
        'step_index': step_index,
    })

def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart = request.session.get('cart', {})
    str_id = str(pk)
    
    quantity = int(request.POST.get('quantity', 1))
    if str_id in cart:
        cart[str_id] += quantity
    else:
        cart[str_id] = quantity
        
    request.session['cart'] = cart
    messages.success(request, f'Added "{product.name}" to your cart.')
    
    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or 'cart_detail'
    return redirect(next_url)

def update_cart(request, pk):
    str_id = str(pk)
    cart = request.session.get('cart', {})
    
    if str_id in cart:
        action = request.POST.get('action')
        if action == 'increase':
            cart[str_id] += 1
        elif action == 'decrease':
            cart[str_id] -= 1
            if cart[str_id] <= 0:
                del cart[str_id]
        elif 'quantity' in request.POST:
            qty = int(request.POST.get('quantity', 1))
            if qty > 0:
                cart[str_id] = qty
            else:
                del cart[str_id]
        request.session['cart'] = cart
        messages.info(request, "Cart updated successfully.")

    return redirect('cart_detail')

def remove_from_cart(request, pk):
    str_id = str(pk)
    cart = request.session.get('cart', {})
    
    if str_id in cart:
        del cart[str_id]
        request.session['cart'] = cart
        messages.info(request, "Item removed from cart.")

    return redirect('cart_detail')

def cart_detail(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0

    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(pk=int(product_id))
            item_total = product.price * quantity
            total_price += item_total
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'item_total': item_total
            })
        except Product.DoesNotExist:
            continue

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'cart.html', context)

def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.warning(request, "Your cart is empty.")
        return redirect('home')

    cart_items = []
    total_price = 0
    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(pk=int(product_id))
            item_total = product.price * quantity
            total_price += item_total
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'item_total': item_total
            })
        except Product.DoesNotExist:
            continue

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')

        if full_name and email and address and city:
            tracking_no = generate_tracking_number()
            order = Order.objects.create(
                full_name=full_name,
                email=email,
                phone=phone,
                address=address,
                city=city,
                total_price=total_price,
                status='Processing',
                tracking_number=tracking_no,
                is_paid=True
            )
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['product'].price,
                    quantity=item['quantity']
                )

            # Clear session cart
            request.session['cart'] = {}
            messages.success(request, f"Order #{order.id} confirmed! Tracking code: {tracking_no}")
            return redirect('order_success', order_id=order.id)
        else:
            messages.error(request, "Please fill in all required fields.")

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'checkout.html', context)

def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order_success.html', {'order': order})


# ==============================================================================
# LUXURY BOUTIQUE ADMIN PORTAL
# ==============================================================================

def admin_portal(request):
    total_revenue = Order.objects.filter(is_paid=True).aggregate(Sum('total_price'))['total_price__sum'] or 0
    total_orders = Order.objects.count()
    total_products = Product.objects.count()
    in_stock_count = Product.objects.filter(in_stock=True).count()
    out_of_stock_count = Product.objects.filter(in_stock=False).count()
    
    processing_orders = Order.objects.filter(status='Processing').count()
    dispatched_orders = Order.objects.filter(status='Inspected & Dispatched').count()
    delivered_orders = Order.objects.filter(status='Delivered').count()
    
    total_reviews = Review.objects.count()
    avg_order_value = int(total_revenue / total_orders) if total_orders > 0 else 0

    orders = Order.objects.all().order_by('-created_at')
    products = Product.objects.all().order_by('-created_at')
    reviews = Review.objects.all().order_by('-created_at')[:25]
    
    categories = [c[0] for c in CATEGORY_CHOICES]
    status_choices = [s[0] for s in ORDER_STATUS_CHOICES]

    context = {
        'total_revenue': total_revenue,
        'total_orders': total_orders,
        'total_products': total_products,
        'in_stock_count': in_stock_count,
        'out_of_stock_count': out_of_stock_count,
        'processing_orders': processing_orders,
        'dispatched_orders': dispatched_orders,
        'delivered_orders': delivered_orders,
        'total_reviews': total_reviews,
        'avg_order_value': avg_order_value,
        'orders': orders,
        'products': products,
        'reviews': reviews,
        'categories': categories,
        'status_choices': status_choices,
    }
    return render(request, 'admin_portal.html', context)

def admin_add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        brand = request.POST.get('brand', '').strip()
        category = request.POST.get('category', 'Luxury')
        price = request.POST.get('price', 0)
        description = request.POST.get('description', '').strip()
        image = request.FILES.get('image')
        is_featured = 'is_featured' in request.POST
        in_stock = 'in_stock' in request.POST

        if name and price:
            prod = Product.objects.create(
                name=name,
                brand=brand or 'Chrono Luxe',
                category=category,
                price=int(price),
                description=description,
                image=image if image else '',
                is_featured=is_featured,
                in_stock=in_stock
            )
            messages.success(request, f'Timepiece "{prod.name}" successfully added to boutique inventory.')
        else:
            messages.error(request, "Name and Price are mandatory fields.")

    return redirect('admin_portal')

def admin_toggle_stock(request, pk):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=pk)
        product.in_stock = not product.in_stock
        product.save()
        status_str = "In Stock" if product.in_stock else "Out of Stock"
        messages.success(request, f'Updated "{product.name}" stock status to: {status_str}.')
    return redirect('admin_portal')

def admin_delete_product(request, pk):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=pk)
        name = product.name
        product.delete()
        messages.success(request, f'Timepiece "{name}" deleted from catalog.')
    return redirect('admin_portal')

def admin_update_order_status(request, pk):
    if request.method == 'POST':
        order = get_object_or_404(Order, pk=pk)
        new_status = request.POST.get('status')
        if new_status in [s[0] for s in ORDER_STATUS_CHOICES]:
            order.status = new_status
            order.save()
            messages.success(request, f'Order #{order.id} status updated to "{new_status}".')
        else:
            messages.error(request, "Invalid order status specified.")
    return redirect('admin_portal')

def admin_delete_review(request, pk):
    if request.method == 'POST':
        review = get_object_or_404(Review, pk=pk)
        review.delete()
        messages.info(request, "Customer review was removed.")
    return redirect('admin_portal')
