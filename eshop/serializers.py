from rest_framework import serializers
from .models import Product,Order,OrderItem,Cart,CartItem, Category
from django.contrib.auth.models import User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category 
        fields = ['id','name','slug']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','name','description','price','category','stock','is_active']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id','user','status','created_at','total']


class OrderItemSerializer(serializers.ModerSerializer):
    class Meta:
        model = OrderItem
        fields = ['id','order','product','quantity','unit_price']


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id','user']


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id','cart','product','quantity']