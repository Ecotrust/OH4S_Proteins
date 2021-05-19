from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('category/<int:category_id>/', views.category),
    re_path('category/$', views.all_categories),
    path('filter_products/<int:category_id>/', views.filterProducts),
    re_path('filter_products/$', views.filterProducts),
    path('filter_providers/<int:category_id>/', views.filterProviders),
    re_path('filter_providers/$', views.filterProviders),
    path('product/<int:product_id>/', views.product),
    path('provider/<int:provider_id>/', views.provider),
    path('results/', views.results),
    path('filter/', views.filter),
]
