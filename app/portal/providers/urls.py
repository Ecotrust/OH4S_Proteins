from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('category/<int:category_id>/', views.category),
    path('filter_products/<int:category_id>/', views.filterProducts),
    path('product/<int:product_id>/', views.product),
    path('provider/<int:provider_id>/', views.provider),
]
