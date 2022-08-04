from django.contrib import admin

from .models import *
# from config.g_model import TimeStampMixin
# Register your models here.

# admin.site.register(TimeStampMixin)
admin.site.register(Variant)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(ProductVariant)
admin.site.register(ProductVariantPrice)