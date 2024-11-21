from django.contrib import admin
# Register your models here.
from .models import Conversation , ConversationMessage
from django.contrib.auth import get_user_model
User = get_user_model


class UnitInLine (admin.TabularInline):
    model = ConversationMessage
    extra = 0 
    can_delete = False


@admin.register(Conversation)
class ConversationAdmin (admin.ModelAdmin):
    list_display = ("sender","receiver","title","created_date")
    search_fields = ("sender__phone_number","receiver__phone_number","title")
    list_display_links = list_display
    inlines = [UnitInLine]

    def has_add_permission(self, request, obj = None): return False
    def has_change_permission(self, request, obj = None): return False