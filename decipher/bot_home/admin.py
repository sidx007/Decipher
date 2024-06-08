from django.contrib import admin
from .models import AuthenticationId, Page

class PageInline(admin.TabularInline):
    model = Page
    extra = 0

class AuthenticationIdAdmin(admin.ModelAdmin):
    inlines = [PageInline]

# Register your models here.
admin.site.register(AuthenticationId, AuthenticationIdAdmin)
admin.site.register(Page)
