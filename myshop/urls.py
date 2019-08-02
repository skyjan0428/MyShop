"""myshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from shop.views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', product_list),
    path('product_list/', product_list),
    path('category/<int:category_id>/', product_list),
    path('product_detail/cart_add/<int:product_id>/', cart_add),
    path('product_detail/cart_remove/<int:product_id>/', cart_remove),
    path('product_detail/<int:product_id>/', product_detail),
    path('cart_detail/', cart_detail),
    path('order_create/', order_create),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
