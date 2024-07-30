from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),  # Maps the root URL (/) to the home view
    path('home/', views.home, name='home'),  # Optional: Explicitly define /home/ URL
    path('coffee-list/', views.coffee_list, name='coffee_list'),  # Example: URL for coffee list
    path('view-cart/', views.view_cart, name='view_cart'),  # Example: URL for view cart
    # Add other URL patterns as needed for additional views


    path('checkout/', views.checkout, name='checkout'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
]