from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from accounts.models import User, Profile
 
 
class UserAdmin(BaseUserAdmin):
    model = User
 
    list_display = (
        "email",
        "role",
        "plan_type",
        "is_plan_paid",
        "plan_start_date",
        "plan_end_date",
        "is_active",
        "total_time",
    )
 
    search_fields = ("email",)
    ordering = ("email",)
 
    #  Edit user page
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {
            "fields": ("role", "is_active", "is_staff", "is_superuser", "groups", "user_permissions")
        }),
        ("Plan Info", {
            "fields": (
                "plan_type",
                "is_plan_paid",
                "plan_start_date",
                "plan_end_date",
            )
        }),
        ("Important dates", {"fields": ("last_login",)}),
    )
 
    # ADD USER PAGE (VERY IMPORTANT FIX)
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "role", "is_active", "is_staff", "is_superuser"),
        }),
    )
 
    readonly_fields = ("plan_start_date", "plan_end_date")
    filter_horizontal = ("groups", "user_permissions")
 
 
admin.site.register(User, UserAdmin)
 

admin.site.register(Profile)
