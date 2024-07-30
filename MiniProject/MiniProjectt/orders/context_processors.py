from .models import CartItem

def cart_summary(request):
    if request.session.session_key:
        cart_items = CartItem.objects.filter(session_id=request.session.session_key)
        total_items = sum(item.quantity for item in cart_items)
        total_price = sum(item.coffee.price * item.quantity for item in cart_items)
    else:
        total_items = 0
        total_price = 0
    
    return {
        'cart_total_items': total_items,
        'cart_total_price': total_price,
    }