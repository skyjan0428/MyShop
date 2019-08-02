from django.contrib import admin

# Register your models here.

from .models import Category, Product, OrderItem, Order

class CategoryAdmin(admin.ModelAdmin):
	list_display = ['name']

admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
	list_display = ['name', 'price', 'stock', 'available', 'created', 'updated']
	list_filter = ['available', 'created', 'updated']
	list_editable = ['price', 'stock', 'available']

admin.site.register(Product, ProductAdmin)


class OrderItemInline(admin.TabularInline):
	model = OrderItem
	raw_id_fields = ['product']


class OrderAdmin(admin.ModelAdmin):
	list_display = ['id', 'first_name', 'last_name', 'email', 'address', 'paid', 'created', 'updated']
	list_filter = ['paid', 'created', 'updated']
	inlines = [OrderItemInline]

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)

