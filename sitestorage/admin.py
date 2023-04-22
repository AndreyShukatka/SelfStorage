from django.contrib import admin
from django.utils.html import format_html

from .models import User, Cargo, Storage, StorageAddress, Order, PaymentOrder


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
    )


@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'get_image_preview'
    )

    def get_image_preview(self, obj):
        if not obj.photo or not obj.id:
            return 'нет картинки'
        return format_html('<img src="{src}" style="max-height: 50px;"/>', src=obj.photo.url)


admin.site.register(Cargo)
admin.site.register(Order)
admin.site.register(StorageAddress)
admin.site.register(PaymentOrder)
