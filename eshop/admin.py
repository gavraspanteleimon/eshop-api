from django.contrib import admin

from eshop.models import Category, Product, Cart, CartItem, Order, OrderItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'is_active')
    search_fields = ('name','category__name',)

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields =('user__username',)

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart','product','quantity')
    search_fields = ('cart__user__username','product__name',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user','status','created_at','total')
    search_fields = ('user__username','status',)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order','product','quantity','unit_price')
    search_fields = ('order__user__username','product__name',)



# Register your models here.
