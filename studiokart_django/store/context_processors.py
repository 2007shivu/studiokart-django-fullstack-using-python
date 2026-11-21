from .models import CartItem, WishlistItem

def store_counts(request):
    if request.user.is_authenticated:
        c_count = sum(item.quantity for item in CartItem.objects.filter(user=request.user))
        w_count = WishlistItem.objects.filter(user=request.user).count()
    else:
        c_count = 0
        w_count = 0
    return {'cart_count': c_count, 'wishlist_count': w_count}
