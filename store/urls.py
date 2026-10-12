from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('product/<int:pk>/add-review/', views.add_review, name='add_review'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('wishlist/toggle/<int:pk>/', views.toggle_wishlist, name='toggle_wishlist'),
    path('track-order/', views.track_order, name='track_order'),
    path('add-to-cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('update-cart/<int:pk>/', views.update_cart, name='update_cart'),
    path('remove-from-cart/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-success/<int:order_id>/', views.order_success, name='order_success'),
    
    # Custom Luxury Admin Portal
    path('admin-portal/', views.admin_portal, name='admin_portal'),
    path('admin-portal/product/add/', views.admin_add_product, name='admin_add_product'),
    path('admin-portal/product/<int:pk>/toggle-stock/', views.admin_toggle_stock, name='admin_toggle_stock'),
    path('admin-portal/product/<int:pk>/delete/', views.admin_delete_product, name='admin_delete_product'),
    path('admin-portal/order/<int:pk>/status/', views.admin_update_order_status, name='admin_update_order_status'),
    path('admin-portal/review/<int:pk>/delete/', views.admin_delete_review, name='admin_delete_review'),
]