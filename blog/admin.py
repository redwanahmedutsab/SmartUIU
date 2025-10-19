from django.contrib import admin
from .models import Tag, Blog, Comment, Reply, LikeDislike, Notification


# -----------------------------
# Inline: Comments inside Blog
# -----------------------------
class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1
    fields = ('author', 'content', 'created_at')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)


# -----------------------------
# Inline: Replies inside Comment
# -----------------------------
class ReplyInline(admin.TabularInline):
    model = Reply
    extra = 1
    fields = ('author', 'content', 'parent_reply', 'created_at')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)


# -----------------------------
# Tag Admin
# -----------------------------
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


# -----------------------------
# Blog Admin
# -----------------------------
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at')
    list_filter = ('created_at', 'tags')
    search_fields = ('title', 'content', 'author__username', 'tags__name')
    ordering = ('-created_at',)
    filter_horizontal = ('tags',)
    inlines = [CommentInline]
    readonly_fields = ('created_at', 'updated_at')


# -----------------------------
# Comment Admin
# -----------------------------
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('blog', 'author', 'short_content', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content', 'author__username', 'blog__title')
    ordering = ('-created_at',)
    inlines = [ReplyInline]
    readonly_fields = ('created_at',)

    def short_content(self, obj):
        return obj.content[:50] + ('...' if len(obj.content) > 50 else '')
    short_content.short_description = 'Content'


# -----------------------------
# Reply Admin
# -----------------------------
@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ('author', 'parent_comment', 'short_content', 'created_at')
    search_fields = ('content', 'author__username', 'comment__content')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

    def parent_comment(self, obj):
        if obj.comment:
            return f"Comment #{obj.comment.id}"
        elif obj.parent_reply:
            return f"Reply #{obj.parent_reply.id}"
        return "None"
    parent_comment.short_description = "Parent"

    def short_content(self, obj):
        return obj.content[:50] + ('...' if len(obj.content) > 50 else '')
    short_content.short_description = 'Content'


# -----------------------------
# Like / Dislike Admin
# -----------------------------
@admin.register(LikeDislike)
class LikeDislikeAdmin(admin.ModelAdmin):
    list_display = ('blog', 'user', 'reaction')
    list_filter = ('reaction',)
    search_fields = ('blog__title', 'user__username')
    ordering = ('blog',)
    list_editable = ('reaction',)


# -----------------------------
# Notification Admin
# -----------------------------
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'blog', 'created_at', 'is_read')
    list_filter = ('is_read',)
    search_fields = ('user__username', 'message', 'blog__title')
    ordering = ('-created_at',)
    list_editable = ('is_read',)