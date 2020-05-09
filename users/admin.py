from django.contrib import admin
# from django.contrib.auth.models import Group
from django.utils.translation import ugettext as _
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),

        (_('Personal info'), {'fields': (
            'first_name',
            'last_name',
        )
        }),
        (_('Permissions'), {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
            )}
         ),
        (_('Important dates'), {
            'fields': ('last_login',)
        }),
    )
    form = UserChangeForm

    search_fields = ('first_name', 'last_name', 'email', 'telegram_username')
    list_display = (
        'email',
        'is_superuser',
        'first_name',
        'last_name',
    )
    ordering = ('email',)


# admin.site.unregister(Group)
