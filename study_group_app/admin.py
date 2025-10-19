from django.contrib import admin
from .models import Group, GroupMember, Message, NotificationStudy


class GroupMemberInline(admin.TabularInline):
    model = GroupMember
    extra = 1
    fields = ('user', 'role', 'date_joined')
    readonly_fields = ('date_joined',)
    autocomplete_fields = ['user']


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    fields = ('sender', 'content', 'file', 'timestamp')
    readonly_fields = ('timestamp',)
    autocomplete_fields = ['sender']


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator', 'member_count')
    search_fields = ('name', 'description', 'creator__username')
    readonly_fields = ()
    inlines = [GroupMemberInline, MessageInline]
    ordering = ('name',)

    def member_count(self, obj):
        return obj.group_members.count()
    member_count.short_description = "Members"


@admin.register(GroupMember)
class GroupMemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'group', 'role', 'date_joined')
    list_filter = ('role', 'date_joined')
    search_fields = ('user__username', 'group__name')
    readonly_fields = ('date_joined',)
    autocomplete_fields = ['user', 'group']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'group', 'short_content', 'timestamp')
    list_filter = ('timestamp', 'group')
    search_fields = ('sender__username', 'content', 'group__name')
    readonly_fields = ('timestamp',)
    autocomplete_fields = ['sender', 'group']

    def short_content(self, obj):
        if obj.content:
            return (obj.content[:50] + '...') if len(obj.content) > 50 else obj.content
        elif obj.file:
            return obj.file.name
        return "-"
    short_content.short_description = "Message"


@admin.register(NotificationStudy)
class NotificationStudyAdmin(admin.ModelAdmin):
    list_display = ('user', 'group_name', 'short_message', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('user__username', 'group_name', 'message_content')
    readonly_fields = ('created_at',)
    actions = ['mark_as_read']

    def short_message(self, obj):
        return (obj.message_content[:50] + '...') if len(obj.message_content) > 50 else obj.message_content
    short_message.short_description = "Message"

    @admin.action(description="Mark selected notifications as read ✅")
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f"{updated} notification(s) marked as read.")