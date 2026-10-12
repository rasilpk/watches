from django.contrib import admin
from .models import Product, Order, OrderItem, Review

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'category', 'price', 'is_featured', 'in_stock')
    list_filter = ('category', 'brand', 'is_featured', 'in_stock')
    search_fields = ('name', 'brand', 'description')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'email', 'status', 'total_price', 'tracking_number', 'created_at', 'is_paid')
    list_filter = ('status', 'is_paid', 'created_at')
    search_fields = ('full_name', 'email', 'tracking_number', 'city')
    inlines = [OrderItemInline]

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'author', 'rating', 'title', 'is_verified', 'created_at')
    list_filter = ('rating', 'is_verified', 'created_at')
    search_fields = ('author', 'title', 'comment', 'product__name')

admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Review, ReviewAdmin)

