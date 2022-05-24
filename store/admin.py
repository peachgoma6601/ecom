from django.contrib import admin
from .models import Product,ProductVariation
# Register your models here.

class ProductsAdmin(admin.ModelAdmin):
    list_display = ('product_name','price','stock','catagory','modified_date','is_available')
    prepopulated_fields ={'slug':('product_name',)}

class VariationAdmin(admin.ModelAdmin):
    list_display  = ('product','variation_catagory','variation_value','is_active')
    list_editable = ('is_active',)
    list_filter = ('product','variation_catagory','variation_value')

admin.site.register(Product,ProductsAdmin)
admin.site.register(ProductVariation,VariationAdmin)