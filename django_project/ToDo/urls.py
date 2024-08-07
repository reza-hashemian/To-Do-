from django.urls import path, include
from .api.board_api import BoardViewSetAPI
from .api.todolist_api import ToDoListViewSetAPI
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('board', BoardViewSetAPI, basename='Board-view-set')
# router.register('todo-list/(?P<board_id>[^/.]+)', ToDoListViewSetAPI, basename='ToDo-list-view-set')
router.register('todo-list/<uuid:board_id>', ToDoListViewSetAPI, basename='ToDo-list-view-set')



urlpatterns = [
    # path('test/', Home.as_view()),
   path('', include(router.urls))
]
