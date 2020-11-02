from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.dashboard, name = 'dashboard'),

    path('products/', views.products, name = 'products'),
    path('create_product/', views.create_product, name = 'create_product'),
    path('update_product/<int:pk>/', views.update_product, name = 'update_product'),
    path('delete_product/<int:pk>/', views.delete_product, name = 'delete_product'),

    path('customer/<int:pk>/', views.customer, name = 'customer'),
    path('customer/new/', views.create_customer, name = 'create_customer'),

    path('create_order/<int:pk>/', views.create_order, name = 'create_order'),
    path('update_order/<int:pk>/', views.update_order, name = 'update_order'),
    path('delete_order/<int:pk>/', views.delete_order, name = 'delete_order'),

    path('accounts/', include('django.contrib.auth.urls')),

    path('create_user/', views.create_user, name = "create_user"),
]
