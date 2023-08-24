from rest_framework import serializers
from .models import MenuItem, Cart, Order, OrderItem, Category
from django.contrib.auth.models import User

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'
        
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        
class CartSerializer(serializers.ModelSerializer):
    #user= serializers.ReadOnlyField()
    menu_item_name = serializers.SerializerMethodField()
    class Meta:
        model = Cart
        fields = ['menu_item', 'menu_item_name','quantity','unit_price','price']
        read_only_fields = ['unit_price','price']
    def get_menu_item_name(self, obj):
        return obj.menu_item.title
        
      
        
class OrderItemsSerializer(serializers.ModelSerializer):
    menu_item_name = serializers.SerializerMethodField()
    class Meta:
        model = OrderItem
        fields = ['menu_item', 'menu_item_name','quantity', 'unit_price', 'price']
        read_only_fields = ['unit_price','price']
        
    def get_menu_item_name(self, obj):
        return obj.menu_item.title
    
class OrderSerializer(serializers.ModelSerializer):
    menu_items = OrderItemsSerializer(source='orderitem_set', many=True, read_only=True)
    user_name = serializers.SerializerMethodField()
    class Meta:
        model = Order
        fields = ['id', 'user', 'user_name', 'delivery_crew', 'status', 'total','date', 'menu_items']
        read_only_fields = ['total','user']
        
    def get_user_name(self, obj):
        return obj.user.username

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'