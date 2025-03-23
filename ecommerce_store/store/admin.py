from django.contrib import admin
from .models import Category, Product
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .forms import CustomerRegisterForm

admin.site.register(Category)
admin.site.register(Product)


#username:Flizon
#mail:flizon@gmail.com
#password:Ecommerce_Store

class CustomUserAdmin(UserAdmin):
    add_form = CustomerRegisterForm
    form = CustomerRegisterForm

    list_display = ('username', 'email', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('username',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )

# Unregister the default User admin and register your custom admin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)