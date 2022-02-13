from django.urls import path
from django.views.decorators.cache import cache_page

from ordersapp import views as ordersapp

app_name = 'ordersapp'

urlpatterns = [
    path('', ordersapp.OrderListView.as_view(), name='list'),
    path('create/', ordersapp.OrderCreateView.as_view(), name='create'),
    path('update/<int:pk>/', ordersapp.OrderUpdateView.as_view(), name='update'),
    path('read/<int:pk>/', cache_page(3600)(ordersapp.OrderDetailView.as_view()), name='read'),
    path('delete/<int:pk>/', ordersapp.OrderDeleteView.as_view(), name='delete'),
    path('complete/<int:pk>/', ordersapp.complete, name='complete'),
    path('product/<int:pk>/price/', ordersapp.get_product_price, name='product_price'),
]
