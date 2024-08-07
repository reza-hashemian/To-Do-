from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import NotFound
from drf_spectacular.utils import extend_schema

from django_project.api.mixins import ApiAuthMixin

from ..models.boards import Board
from ..models.todolist import ToDoList


@extend_schema(tags=['Todolist'])
class ToDoListViewSetAPI(ApiAuthMixin, ModelViewSet):
    class ToDOListSerializer(ModelSerializer):
        class Meta:
            model = ToDoList
            fields = ['id', 'name', 'color']
    serializer_class = ToDOListSerializer
    queryset = ToDoList.objects.all()

    def perform_create(self, serializer):
        board_id = self.kwargs['board_id']
        try:
            board = self.request.user.boards.get(id=board_id)
        except Board.DoesNotExist:
            raise NotFound('Board not found')
        serializer.save(board=board)

    def get_queryset(self):
        board_id = self.kwargs['board_id']
        try:
            Board.objects.get(id=board_id)
        except Board.DoesNotExist:
            raise NotFound('Board not found')
        return self.queryset.filter(board__in=self.request.user.boards.
                                       filter(id=board_id).values_list('id', flat=True))

