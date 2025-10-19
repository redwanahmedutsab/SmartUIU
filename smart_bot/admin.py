from django.contrib import admin
from .models import ChatSession, ChatMessage


class ChatMessageInline(admin.TabularInline):
    model = ChatMessage
    extra = 0
    fields = ('sender', 'text', 'file', 'created_at')
    readonly_fields = ('created_at',)
    ordering = ('created_at',)


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'session_id', 'created_at')
    search_fields = ('title', 'user__username', 'session_id')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)
    inlines = [ChatMessageInline]
    ordering = ('-created_at',)


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('chat', 'sender', 'short_text', 'created_at')
    list_filter = ('sender', 'created_at')
    search_fields = ('chat__title', 'text', 'chat__user__username')
    readonly_fields = ('created_at',)
    ordering = ('created_at',)

    def short_text(self, obj):
        return obj.text[:70] + ('...' if len(obj.text) > 70 else '')
    short_text.short_description = "Message Preview"