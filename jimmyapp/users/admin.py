from pyexpat import model
from django.contrib import admin
from users.models import User, Establishment, Address, Order, Settings




# Register your models here.
class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = ['name','surname','email', 'phone', 'address']

admin.site.register(User, UserAdmin)

class EstablishmentAdmin(admin.ModelAdmin):
    model = Establishment
    list_display = ['companyname','name','surname','email', 'phone', 'address']

admin.site.register(Establishment, EstablishmentAdmin)

class AddressAdmin(admin.ModelAdmin):
    model = Address
    fields = ['address_line_1', 'address_line_2', 'town', 'city', 'post_code']

admin.site.register(Address, AddressAdmin)

class OrderAdmin(admin.ModelAdmin):
    model = Order
    fields = ['number', 'user', 'establishment', 'comment', 'stuart_delivery_fee', 'stuart_tracking_url', 'stuart_pickup', 'stuart_delivery_distance','stuart_delivery_duration', 'stuart_delivery_id' , 'stuart_delivery_status']

admin.site.register(Order, OrderAdmin)


class SettingsAdmin(admin.ModelAdmin):
       model = Settings
       fields = ['name', 'websocket']

admin.site.register(Settings, SettingsAdmin)



