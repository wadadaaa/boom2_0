from django.contrib import admin

from apps.mainpage.models import  Seller, Product, Category, Subcategory

class SellerAdmin(admin.ModelAdmin):
    #name => slug automatical
    prepopulated_fields = {"slug":("name",)}

    #wich fields to display
    list_display = ('name', 'description')
    list_display_links = ('name',)
    list_filter = ('name',)

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug":("name",)}
    list_display = ('name', 'description', 'publish_at','seller')
    list_display_links = ('name',)
    list_filter = ('name','price')
    search_fields = ['name', 'description', 'seller__name',
                     'category__name']
    fieldsets = (
        (None, {
            'fields':('name', 'slug'),
        }),
        ('Description', {
            'fields':('description', 'price', 'seller' ,
                'category')
        }),
        ('Publication', {
            'fields':('active', 'publish_at')
        })


    )

class CategoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(Seller,SellerAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Category,CategoryAdmin)
