import os

from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import NotFound, PermissionDenied
from drf_spectacular.utils import extend_schema
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from django_project.api.mixins import ApiAuthMixin
from config.django.base import MEDIA_ROOT

from ..models.todolist import ToDoList
from ..models.tasks import Task, Label, Emoji, Comment, Attachments, ChecklistItem


@extend_schema(tags=['Task'])
class TaskViewSetAPI(ApiAuthMixin, ModelViewSet):
    class TaskSerializer(ModelSerializer):
        class Meta:
            model = Task
            fields = ['id', 'name', 'description',
                      'should_done_at', 'done_at',
                      'status', 'label',
                      'latitude', 'longitude',
                      'priority']

    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def perform_create(self, serializer):
        todolist_id = self.kwargs['todolist_id']
        try:
            todo_list = ToDoList.objects.get(id=todolist_id)
            if todo_list.board.baseuser == self.request.user:
                serializer.save(todolist=todo_list)
            else:
                raise PermissionDenied('this todolist_id is invalid')
        except ToDoList.DoesNotExist:
            raise NotFound('Todo not found')

    def get_queryset(self):
        todolist_id = self.kwargs['todolist_id']
        try:
            todo_list = ToDoList.objects.get(id=todolist_id)
            if not (todo_list.board.baseuser == self.request.user):
                raise PermissionDenied('this todolist_id is invalid')
        except ToDoList.DoesNotExist:
            raise NotFound('Todo not found')
        return self.queryset.filter(todolist=todo_list)



@extend_schema(tags=['Label'])
class LabelViewSetAPI(ApiAuthMixin, ModelViewSet):
    class TaskSerializer(ModelSerializer):
        class Meta:
            model = Label
            fields = ['id', 'name', 'color']

    queryset = Label.objects.all()
    serializer_class = TaskSerializer



@extend_schema(tags=['Task/checklist'])
class ChecklistItemViewSetAPI(ApiAuthMixin, ModelViewSet):
    class ChecklistItemSerializer(ModelSerializer):
        class Meta:
            model = ChecklistItem
            fields = ['id', 'description', 'is_completed']

    queryset = ChecklistItem.objects.all()
    serializer_class = ChecklistItemSerializer

    def perform_create(self, serializer):
        task_id = self.kwargs['task_id']
        try:
            task = Task.objects.get(id=task_id)
            if task.todolist.board.baseuser == self.request.user:
                serializer.save(task=task, owner=self.request.user)
            else:
                raise PermissionDenied('this task_id is invalid')
        except Task.DoesNotExist:
            raise NotFound('Task not found')

    def get_queryset(self):
        task_id = self.kwargs['task_id']
        try:
            task = Task.objects.get(id=task_id)
            if not(task.todolist.board.baseuser == self.request.user):
                raise PermissionDenied('this task_id is invalid')
        except Task.DoesNotExist:
            raise NotFound('Task not found')
        return self.queryset.filter(task=task)


@extend_schema(tags=['Task/Comment'])
class CommentViewSetAPI(ApiAuthMixin, ModelViewSet):
    class CommentSerializer(ModelSerializer):
        class Meta:
            model = Comment
            fields = ['id', 'text']

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        task_id = self.kwargs['task_id']
        try:
            task = Task.objects.get(id=task_id)
            if task.todolist.board.baseuser == self.request.user:
                serializer.save(task=task, owner=self.request.user)
            else:
                raise PermissionDenied('this task_id is invalid')
        except Task.DoesNotExist:
            raise NotFound('Task not found')

    def get_queryset(self):
        task_id = self.kwargs['task_id']
        try:
            task = Task.objects.get(id=task_id)
            if not(task.todolist.board.baseuser == self.request.user):
                raise PermissionDenied('this task_id is invalid')
        except Task.DoesNotExist:
            raise NotFound('Task not found')
        return self.queryset.filter(task=task)


@extend_schema(tags=['Task/Attachments'])
class AttachmentsViewSetAPI(ApiAuthMixin, mixins.CreateModelMixin,
                            mixins.ListModelMixin, mixins.DestroyModelMixin,
                            mixins.RetrieveModelMixin, GenericViewSet):
    class AttachmentsSerializer(ModelSerializer):
        class Meta:
            model = Attachments
            fields = ['id', 'file']

    queryset = Attachments.objects.all()
    serializer_class = AttachmentsSerializer

    def perform_create(self, serializer):

        def save_file_to_media_dir(f, sub_directory):
            try:
                os.makedirs(sub_directory)
            except:
                ...
            with open(os.path.join(sub_directory, f.name), 'wb+') as destinations:
                for chunk in f.chunks():
                    destinations.write(chunk)

        for field in self.request.FILES.keys():
                for formfile in self.request.FILES.getlist(field):
                    sub_directory = os.path.join(MEDIA_ROOT, 'Attachments')
                    sub_directory = os.path.join(MEDIA_ROOT, f'{self.request.user.id}')
                    save_file_to_media_dir(formfile, sub_directory)
        file_path = os.path.join(sub_directory.removeprefix(MEDIA_ROOT), formfile.name)

        task_id = self.kwargs['task_id']

        try:
            task = Task.objects.get(id=task_id)
            if task.todolist.board.baseuser == self.request.user:
                serializer.save(task=task, user=self.request.user, file=file_path)
            else:
                raise PermissionDenied('this task_id is invalid')
        except Task.DoesNotExist:
            raise NotFound('Task not found')

    def get_queryset(self):
        task_id = self.kwargs['task_id']
        try:
            task = Task.objects.get(id=task_id)
            if not(task.todolist.board.baseuser == self.request.user):
                raise PermissionDenied('this task_id is invalid')
        except Task.DoesNotExist:
            raise NotFound('Task not found')
        return self.queryset.filter(task=task)


@extend_schema(tags=['Task/Emoji'])
class EmojiViewSetAPI(ApiAuthMixin, ModelViewSet):
    class EmojiSerializer(ModelSerializer):
        class Meta:
            model = Emoji
            fields = ['id', 'emoji']

    queryset = Emoji.objects.all()
    serializer_class = EmojiSerializer

    def perform_create(self, serializer):
        comment_id = self.kwargs['comment_id']
        try:
            comment = Comment.objects.get(id=comment_id)
            if comment.task.todolist.board.baseuser == self.request.user:
                serializer.save(comment=comment, user=self.request.user)
            else:
                raise PermissionDenied('this comment_id is invalid')
        except Comment.DoesNotExist:
            raise NotFound('Task not found')

    def get_queryset(self):
        comment_id = self.kwargs['comment_id']

        try:
            comment = Comment.objects.get(id=comment_id)
            if not(comment.task.todolist.board.baseuser == self.request.user):
                raise PermissionDenied('this comment_id is invalid')
        except Comment.DoesNotExist:
            raise NotFound('Task not found')
        return self.queryset.filter(comment=comment)