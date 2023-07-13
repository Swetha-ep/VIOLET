from django.contrib import admin
from.models import *
# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name','description','slug']
    prepopulated_fields={'slug':('category_name',)}

admin.site.register(Category)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name','selling_price','original_price', 'category', 'modified_date', 'is_available')
    prepopulated_fields={'slug':('product_name',)}

admin.site.register(Product)

admin.site.register(Banner)

admin.site.register(Offer)
admin.site.register(Size)