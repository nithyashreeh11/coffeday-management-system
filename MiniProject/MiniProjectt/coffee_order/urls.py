from django.contrib import admin
from django.urls import path, include
from orders import views 

urlpatterns = [
  
    path('admin/', admin.site.urls),
    path('', include('orders.urls')),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
]