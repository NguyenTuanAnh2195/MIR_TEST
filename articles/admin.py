from django.contrib import admin

# Register your models here.
from .models import Article, ContactRequest


class ContactRequestAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


admin.site.register(Article)
admin.site.register(ContactRequest, ContactRequestAdmin)
