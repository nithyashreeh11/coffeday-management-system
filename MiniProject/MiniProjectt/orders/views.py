from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Coffee, CartItem
import json

# myapp/views.py

from django.shortcuts import render


def home(request):
    # Any logic you need can go here
    return render(request, 'home.html')



def coffee_list(request):
    coffees = Coffee.objects.all()
    return render(request, 'orders/coffee_list.html', {'coffees': coffees})

def add_to_cart(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        coffee_id = data.get('coffee_id')
        quantity = data.get('quantity', 1)
        
        coffee = Coffee.objects.get(id=coffee_id)
        session_id = request.session.session_key
        if not session_id:
            request.session.create()
            session_id = request.session.session_key
        
        cart_item, created = CartItem.objects.get_or_create(
            coffee=coffee,
            session_id=session_id,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        # Calculate updated cart summary
        cart_items = CartItem.objects.filter(session_id=session_id)
        cart_total_items = sum(item.quantity for item in cart_items)
        cart_total_price = sum(item.coffee.price * item.quantity for item in cart_items)
        
        return JsonResponse({
            'success': True,
            'cart_total_items': cart_total_items,
            'cart_total_price': cart_total_price
        })
    return JsonResponse({'success': False})

def view_cart(request):
    session_id = request.session.session_key
    cart_items = CartItem.objects.filter(session_id=session_id)
    total = sum(item.coffee.price * item.quantity for item in cart_items)
    return render(request, 'orders/cart.html', {'cart_items': cart_items, 'total': total})

def checkout(request):
    if request.method == 'POST':
        # Process the order (you can add more logic here)
        session_id = request.session.session_key
        CartItem.objects.filter(session_id=session_id).delete()
        return render(request, 'orders/order_confirmation.html')
    return redirect('view_cart')

@require_POST
def remove_from_cart(request, item_id):
    try:
        cart_item = CartItem.objects.get(id=item_id, session_id=request.session.session_key)
        cart_item.delete()
        
        # Recalculate cart totals
        cart_items = CartItem.objects.filter(session_id=request.session.session_key)
        cart_total_items = sum(item.quantity for item in cart_items)
        cart_total_price = sum(item.coffee.price * item.quantity for item in cart_items)
        
        return JsonResponse({
            'success': True,
            'cart_total_items': cart_total_items,
            'cart_total_price': cart_total_price
        })
    except CartItem.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Item not found'})