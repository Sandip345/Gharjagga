from django.contrib import admin
from django.utils.html import format_html
from . import models

from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'available', 'price')
    list_filter = ('active', 'available', 'date_updated')
    list_editable = ('available', )
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}
    autocomplete_fields=('tags',)
admin.site.register(models.Product, ProductAdmin)

class ProductTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    list_filter = ('active',)
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}
admin.site.register(models.ProductTag, ProductTagAdmin)

class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('thumbnail_tag', 'product_name')
    readonly_fields = ('thumbnail',)
    search_fields = ('product__name',)
    def thumbnail_tag(self, obj):
        if obj.thumbnail:
            return format_html('<img src="%s"/>' % obj.thumbnail.url)
        return "-"
    thumbnail_tag.short_description = "Thumbnail"
    def product_name(self, obj):
        return obj.product.name
admin.site.register(models.ProductImage, ProductImageAdmin)


@admin.register(models.User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = (
(None, {"fields": ("email", "password")}),
(
"Personal info",
{"fields": ("first_name", "last_name")},
),
(
"Permissions",
{
"fields": (
"is_active",
"is_staff",
"is_superuser",
"groups",
"user_permissions",
)
},
),
(
"Important dates",
{"fields": ("last_login", "date_joined")},
),
)
    add_fieldsets = (
(
None,
{
"classes": ("wide",),
"fields": ("email", "password1", "password2"),
},
),
)
    list_display = (
"email",
"first_name",
"last_name",
"is_staff",
)
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)
