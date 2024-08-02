from django.contrib import admin

from .models import (Task, ToDoList, MemberJoined,
                     ChecklistItem, Comment, Attachments,
                     Label, Emoji, Board)


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ['name', 'baseuser']
    list_per_page = 20
    search_fields = ['name', 'description', 'baseuser']
    list_display_links = ['name']


class MemberJoinStack(admin.StackedInline):
    model = MemberJoined
    extra = 1


@admin.register(ToDoList)
class ToDoListAdmin(admin.ModelAdmin):
    list_display = ['name', 'priority', 'board']
    list_editable = ['priority']
    list_per_page = 20
    search_fields = ['name', 'description', 'baseuser']
    inlines = [MemberJoinStack]
    list_display_links = ['name']


@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    list_display = ['name', 'color']
    list_editable = ['color']
    list_display_links = ['name']


class EmojiStack(admin.StackedInline):
    model = Emoji
    extra = 1


class CommentStack(admin.StackedInline):
    model = Comment
    extra = 1


class ChecklistItemStack(admin.StackedInline):
    model = ChecklistItem
    raw_id_fields = ['owner', 'user_that_should_done']
    extra = 1


class AttachmentsStack(admin.StackedInline):
    model = Attachments
    raw_id_fields = ['task', 'user']
    extra = 1


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'should_done_at', 'status']
    list_editable = ['status']
    list_display_links = ['name']
    list_per_page = 20
    list_filter = ['status']
    filter_horizontal = ['label']
    raw_id_fields = ['todolist']
    inlines = [CommentStack, ChecklistItemStack,
               AttachmentsStack]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['text', 'user']
    list_per_page = 20
    inlines = [EmojiStack]
    raw_id_fields = ['task', 'user']


@admin.register(Attachments)
class AttachmentsAdmin(admin.ModelAdmin):
    list_display = ['file', 'user']
    list_per_page = 20
    raw_id_fields = ['task', 'user']


@admin.register(Emoji)
class EmojiAdmin(admin.ModelAdmin):
    list_display = ['emoji', 'user']
    list_per_page = 20
    raw_id_fields = ['comment', 'user']


@admin.register(MemberJoined)
class MemberJoinedAdmin(admin.ModelAdmin):
    list_display = ['id', 'baseuser', 'todolist']
    list_per_page = 20


@admin.register(ChecklistItem)
class ChecklistItemAdmin(admin.ModelAdmin):
    list_display = ['description', 'is_completed']
    list_per_page = 20
    raw_id_fields = ['task', 'user_that_should_done', 'owner']

