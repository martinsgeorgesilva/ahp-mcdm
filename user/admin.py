from django.contrib import admin

from user.models import User

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm

class UserCreateForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'occupation' , 'company', )


class UserAdmin(UserAdmin):
    add_form = UserCreateForm
    # prepopulated_fields = {'username': ('first_name' , 'last_name', )}

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('occupation', 'company', 'username', 'password1', 'password2', ),
        }),
    )


# Re-register UserAdmin
# admin.site.unregister(User)
admin.site.register(User, UserAdmin)