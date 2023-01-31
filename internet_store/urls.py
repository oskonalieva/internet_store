"""internet_store URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from products.views import products_view, main_view, product_detail_view, categories_view, create_products_view
from django.conf.urls.static import static
from internet_store import settings
from users.views import auth_view, register_view, logout_view
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_view),
    path('products/', products_view),
    path('categories/', categories_view),
    path('products/<int:id>/', product_detail_view),
    path('products/create/', create_products_view),

    #users
    path('users/login/', auth_view),
    path('users/register/', register_view),
    path('users/logout/', logout_view),



]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
