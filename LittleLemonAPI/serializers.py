from datetime import datetime

from rest_framework import serializers

from .models import (
    MenuItem,
    User,
    Cart,
    Order,
    OrderItem,
)


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category']
        
        
class UserSerializer(serializers.ModelSerializer):
    Date_Joined = serializers.SerializerMethodField()
    date_joined = serializers.DateTimeField(write_only=True, default=datetime.now())
    email = serializers.EmailField(required=False)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'date_joined', 'Date_Joined']
        
    def get_Date_Joined(self, obj):
        return obj.date_joined.strftime('%Y-%m-%d')
    
    
class CartSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='menuitem.title', read_only=True)
    unit_price = serializers.DecimalField(max_digits=6, decimal_places=2, source='menuitem.price', read_only=True)
    
    class Meta:
        model = Cart
        fields = ['user_id', 'menuitem', 'name', 'quantity', 'unit_price', 'price']
        extra_kwargs = {
            'price': { 
                'read_only': True,
            },
        }


class OrderSerializer(serializers.ModelSerializer):
    Date = serializers.SerializerMethodField()
    date = serializers.DateTimeField(write_only=True, default=datetime.now)
    order_items = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = ['id', 'user', 'delivery_crew', 'status', 'total', 'Date', 'date', 'order_items']
        extra_kwargs = {
            'total': {
                'read_only': True,
            },
            'user': {
                'read_only': True,
            }
        }
        
    def get_Date(self, obj):
        return obj.date.strftime('%Y-%m-%d')
    
    def get_order_items(self, obj):
        order_items = OrderItem.objects.filter(order=obj)
        serializers = OrderItemSerializer(order_items, many=True, context={'request': self.context['request']})
        return serializers.data
    
    
class OrderItemSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='menuitem.title', read_only=True)
    price = serializers.DecimalField(max_digits=6, decimal_places=2, read_only=True)
    unit_price = serializers.DecimalField(source='menuitem.price', max_digits=6, decimal_places=2, read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['name', 'quantity', 'unit_price', 'price']
        extra_kwargs = {
            'menuitem': {
                'read_only': True,
            }
        }