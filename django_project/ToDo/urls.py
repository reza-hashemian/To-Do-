from django.urls import path, include
from .api.board_api import BoardViewSetAPI
from .api.todolist_api import ToDoListViewSetAPI
from rest_framework.routers import DefaultRouter
from .api.tasks_api import (TaskViewSetAPI,
                            ChecklistItemViewSetAPI,
                            CommentViewSetAPI,
                            AttachmentsViewSetAPI,
                            EmojiViewSetAPI,
                            )


router = DefaultRouter()
router.register('board', BoardViewSetAPI, basename='Board-view-set')
router.register('todo-list/(?P<board_id>[^/.]+)', ToDoListViewSetAPI, basename='ToDo-list-view-set')
router.register('task/(?P<todolist_id>[^/.]+)', TaskViewSetAPI, basename='Task-view-set')
router.register('ChecklistItem/(?P<task_id>[^/.]+)', ChecklistItemViewSetAPI, basename='ChecklistItem-view-set')
router.register('Comment/(?P<task_id>[^/.]+)', CommentViewSetAPI, basename='comment-view-set')
router.register('Attachments/(?P<task_id>[^/.]+)', AttachmentsViewSetAPI, basename='attachment-view-set')
router.register('Emoji/(?P<comment_id>[^/.]+)', EmojiViewSetAPI, basename='emoji-view-set')



urlpatterns = [
   path('', include(router.urls)),
]
