from django import template
from django.db.models import Count
from django.http import HttpRequest

from product_module.models import ProductCategory, ProductBrand

register = template.Library()


@register.inclusion_tag('product_module/components/product_categories_component.html', takes_context=True)
def product_categories_inclusion(context, *args, **kwargs):
    request: HttpRequest = context.get('request')
    print(f"path is: {request.path}")
    product_categories = ProductCategory.objects.filter(is_active=True, is_delete=False)
    return {'categories': product_categories}


@register.inclusion_tag('product_module/components/product_brands_component.html')
def product_brands_inclusion(*args, **kwargs):
    product_brands = ProductBrand.objects.annotate(products_count=Count('product')).filter(is_active=True)
    return {'brands': product_brands}
