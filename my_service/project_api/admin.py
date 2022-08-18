from django.contrib import admin

from .models import *

class DeviceAdmin(admin.ModelAdmin):
    search_fields = ("manufacturer", "model")
    list_display = ("id", "manufacturer", "model")

class OrderAdmin(admin.ModelAdmin):
    def my_customer(self, obj):
        return obj.device.customer_id.customer_name

    def my_serial_number(self, obj):
        return obj.device.serial_number

    def my_device_model(self, obj):
        return obj.device.analyzer_id.model

    def my_device_manufacturer(self, obj):
        return obj.device.analyzer_id.manufacturer

    my_customer.short_description = "Пользователь"
    my_serial_number.short_description = "Серийный номер"
    my_device_model.short_description = "Модель"
    my_device_manufacturer.short_description = "Производитель"

    list_display = ("id", "my_device_manufacturer", "my_device_model", "my_serial_number", "my_customer",
                    "order_description", "created_at", "updated_at", "order_status")
    search_fields = ("device__customer_id__customer_name", "device__id", "device__serial_number",
                     "device__analyzer_id__model", "device__analyzer_id__manufacturer")
    raw_id_fields = ("device", )

class CustomerAdmin(admin.ModelAdmin):
    search_fields = ("customer_name", "customer_address")
    list_display = ("id", "customer_name", "customer_address", "customer_city")

class DeviceInFieldAdmin(admin.ModelAdmin):
    def my_customer(self, obj):
        return obj.device.customer_id.customer_name

    def my_device_model(self, obj):
        return obj.device.analyzer_id.model

    def my_device_manufacturer(self, obj):
        return obj.device.analyzer_id.manufacturer

    my_customer.short_description = "Пользователь"
    my_device_model.short_description = "Модель"
    my_device_manufacturer.short_description = "Производитель"


    search_fields = ("serial_number", )
    raw_id_fields = ("customer_id", "analyzer_id")
    list_display = ("id", "serial_number", "customer_id", "analyzer_id", "owner_status")


admin.site.register(Order, OrderAdmin)
admin.site.register(Device, DeviceAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(DeviceInField, DeviceInFieldAdmin)