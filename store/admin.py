from django.contrib import admin
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'featured')
    list_editable = ('price', 'stock', 'featured')
    search_fields = ('name',)
    list_filter = ('featured',)

admin.site.register(Product, ProductAdmin)
