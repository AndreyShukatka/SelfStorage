from django.contrib import admin

from .models import User, Cargo, Storage, StorageAddress, Order, PaymentOrder


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
    )


admin.site.register(Cargo)
admin.site.register(Storage)
admin.site.register(Order)
admin.site.register(StorageAddress)
admin.site.register(PaymentOrder)
