from django.contrib import admin
from .import models
# Register your models here.
class productAdmin(admin.ModelAdmin):
   
    list_display = ('id', 'product_name', 'category','brand','model','price','product_image')
    search_fields = ['id','product_name']
    #list_display = ['your fields',]

 
  
    

  
class categoryAdmin(admin.ModelAdmin):
    list_display = ('id','category','category_image')
    search_fields = ['id','category']
  
   
  


class modelsAdmin(admin.ModelAdmin):
    list_display = ('id','brand','category','model_name')
    search_fields = ['id','brand']
 
class brandAdmin(admin.ModelAdmin):
    list_display = ('id','brand_name')
    search_fields = ['id','category']


class cartAdmin(admin.ModelAdmin):
    list_display = ('id','session_key','product')
  

  
admin.site.register(models.category,categoryAdmin)
admin.site.register(models.brand,brandAdmin)
admin.site.register(models.product_model,modelsAdmin)
admin.site.register(models.product,productAdmin)
admin.site.register(models.cart,cartAdmin)
