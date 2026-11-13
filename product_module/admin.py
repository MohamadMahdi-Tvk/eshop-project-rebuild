from django.contrib import admin
from . import models
from guardian.admin import GuardedModelAdmin


@admin.register(models.Product)
class ProductAdmin(GuardedModelAdmin):
    list_filter = ['category', 'is_active']
    list_display = ['title', 'price', 'is_active', 'is_delete']
    list_editable = ['price', 'is_active']


@admin.register(models.ProductCategory)
class ProductCategoryAdmin(GuardedModelAdmin):
    pass


admin.site.register(models.ProductTag)
admin.site.register(models.ProductBrand)
admin.site.register(models.ProductVisit)
admin.site.register(models.ProductGallery)

# ----------------------------------------------------------------------------------------------------
# username & password (admin_panel):

# username: admin_panel
# password: 1234

# username & password (other user):

# username: ----
# password:abc@1234

# ----------------------------------------------------------------------------------------------------
