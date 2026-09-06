from django.contrib import admin
from django.urls import path, include

urlpatterns = [

    path('', include('home_module.urls')),
    path('contact-us/', include('contact_module.urls')),
    path('products/', include('product_module.urls')),
    path('admin/', admin.site.urls)

]
