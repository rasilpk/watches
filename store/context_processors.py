def cart_context(request):
    cart = request.session.get('cart', {})
    total_count = sum(cart.values()) if isinstance(cart, dict) else 0
    wishlist = request.session.get('wishlist', [])
    if not isinstance(wishlist, list):
        wishlist = []
    return {
        'cart_item_count': total_count,
        'wishlist_count': len(wishlist),
        'wishlist_ids': wishlist,
    }
