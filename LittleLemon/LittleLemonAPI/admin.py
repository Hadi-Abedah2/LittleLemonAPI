from typing import Any, Optional
from django.contrib import admin
from .models import Cart, Category, MenuItem, Order, OrderItem
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import ModelAdmin
# Register your models here.

admin.site.register(Cart)
admin.site.register(Category)
#admin.site.register(MenuItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.unregister(User)
@admin.register(User) 
class CustomUserAdmin(UserAdmin):
    readonly_fields = ['last_login', 'date_joined' ]
    
    
@admin.register(MenuItem)    
class CustomMenuItem(ModelAdmin):
    search_fields=['title']
    ordering =['price']
    
    

