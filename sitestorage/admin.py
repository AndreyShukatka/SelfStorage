from django.contrib import admin

from .models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
    )


admin.site.register(Cargo)
admin.site.register(Storage)
admin.site.register(Order)
