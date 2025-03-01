from django.contrib import admin
from orders.models import Order, OrderDetail

# Register your models here.
class OrderDetailInline(admin.TabularInline):
    model = OrderDetail
    fields = ["course", "price", "real_price", "discount_name"]


class OrderModelAdmin(admin.ModelAdmin):
    model = Order
    list_display = ["id","order_number","user","total_price","total_price","order_status"]

admin.site.register(Order, OrderModelAdmin)