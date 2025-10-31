def cart_item_count(request):
    cart = request.session.get('cart', [])
    total_items = sum(item.get('quantity', 1) for item in cart)
    return {'cart_item_count': total_items}

def wishlist_item_count(request):
    wishlist = request.session.get('wishlist', [])
    total_items = len(wishlist)
    return {'wishlist_item_count': total_items}
