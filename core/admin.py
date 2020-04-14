from django.contrib import admin
from django.utils.html import mark_safe   
from .models import (Category,
Coupon,
GalaryImage,
Product,
User,
ProductReview,
SubCategory,
OrderItem,
AddtoCard
)
# Register your models here.

admin.site.site_header = "Weal Shop Dashboard"
admin.site.register(Category)
admin.site.register(Coupon)
admin.site.register(GalaryImage)
admin.site.register(OrderItem)
admin.site.register(AddtoCard)

admin.site.register(User)
admin.site.register(ProductReview)
admin.site.register(SubCategory)

class ProductAdmin(admin.ModelAdmin): 
    def product_thumbnail_image(self, obj): 
        return mark_safe('<img src="{url}" width="30"'.format(url = obj.product_thumbnail.url) 
    )    
    list_display = ['name','product_thumbnail_image','product_cateogry',] 
    prepopulated_fields = {"slug":('name',)}


admin.site.register(Product, ProductAdmin)
