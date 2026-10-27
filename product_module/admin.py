from django.contrib import admin
from . import models


class ProductAdmin(admin.ModelAdmin):
    list_filter = ['category', 'is_active']
    list_display = ['title', 'price', 'is_active', 'is_delete']
    list_editable = ['price', 'is_active']

admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.ProductCategory)
admin.site.register(models.ProductTag)
admin.site.register(models.ProductBrand)
admin.site.register(models.ProductVisit)

# ----------------------------------------------------------------------------------------------------
# username & password (admin):

# username: admin
# password: 1234

# username & password (other user):

# username: ----
# password:abc@1234

# ----------------------------------------------------------------------------------------------------
