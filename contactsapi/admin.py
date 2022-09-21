from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from . import models

class UserAdmin(BaseUserAdmin):

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('name', 'email', 'phone_no')
    list_filter = ('is_admin',)
    fieldsets = (
        ('User Credentials', {'fields': ('phone_no','name', 'password')}),
        ('Personal info', {'fields': ('email',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name','phone_no', 'password1', 'password2'),
        }),
    )
    search_fields = ('phone_no',)
    ordering = ('is_admin',)
    filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(models.User, UserAdmin)


'''Register the phone number model'''
@admin.register(models.PhoneNumber)
class PhoneNoAdmin(admin.ModelAdmin):
  list_display = ['number', 'spam_count']


'''Register the contacts model'''
@admin.register(models.Contact)
class PhoneNoAdmin(admin.ModelAdmin):
  list_display = ['user', 'phone_no', 'name']
