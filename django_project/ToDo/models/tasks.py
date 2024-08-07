from django.db import models

from django_project.common.models import BaseModel
from django_project.users.models import BaseUser

from .todolist import ToDoList


class Label(models.Model):
    class ColorChoice(models.TextChoices):
        BLUE = 'blue', 'blue'
        INDIGO = 'indigo', 'indigo'
        PURPLE = 'purple', 'purple'
        PINK = 'pink', 'pink'
        RED = 'red', 'red'
        ORANGE = 'orange', 'orange'
        YELLOW = 'yellow', 'yellow'
        GREEN = 'green', 'green'
        TEAL = 'teal', 'teal'
        CYAN = 'cyan', 'cyan'

    name = models.CharField(max_length=255)
    color = models.CharField(max_length=30, default=ColorChoice.GREEN,
                             choices=ColorChoice.choices)

    class Meta:
        unique_together = ('name', 'color')

    def __str__(self):
        return f'{self.name}::{self.color}'


class Task(BaseModel):
    class TaskStatus(models.TextChoices):
        NOT_STARTED = 'NOT_STARTED', 'Not Started'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        PENDING = 'PENDING', 'Pending'
        CANCELLED = 'CANCELLED', 'Cancelled'
        DEFERRED = 'DEFERRED', 'Deferred'
        NEEDS_REVIEW = 'NEEDS_REVIEW', 'Needs Review'
        COMPLETED = 'COMPLETED', 'Completed'

    name = models.CharField(max_length=255)
    todolist = models.ForeignKey(ToDoList, on_delete=models.CASCADE,
                                 related_name='tasks', related_query_name='task')
    description = models.TextField(null=True, blank=True)
    should_done_at = models.DateTimeField(null=True, blank=True)
    done_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=TaskStatus.choices, default=TaskStatus.NOT_STARTED)
    label = models.ManyToManyField(Label, related_name='labels', related_query_name='label', blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    priority = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['-priority', 'created_at']

    def __str__(self):
        return (f'name={self.name}::todolist={self.todolist.__str__()}::'
                f'status={self.status}::description={self.description}')


class ChecklistItem(models.Model):
    task = models.ForeignKey(Task, related_name='checklist_items', on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    is_completed = models.BooleanField(default=False)
    owner = models.ForeignKey(BaseUser, related_name='checklists_owner',
                              related_query_name='checklist_owner',
                              on_delete=models.CASCADE)

    def __str__(self):
        return f'task={self.task.__str__()}::owner={self.owner.__str__()}'


class Comment(models.Model):
    task = models.ForeignKey(Task, related_name='comments', on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    user = models.ForeignKey(BaseUser, related_name='comments_of_task', on_delete=models.CASCADE)

    def __str__(self):
        return f'task={self.task.__str__()}::user={self.user.__str__()}::text={self.text}'


class Emoji(models.Model):
    comment = models.ForeignKey(Comment, related_name='emojis', on_delete=models.CASCADE)
    emoji = models.CharField(max_length=10)
    user = models.ForeignKey(BaseUser, related_name='emoji_of_comment_of_task', on_delete=models.CASCADE)

    def __str__(self):
        return f'task={self.task.__str__()}::user={self.user.__str__()}::emoji={self.emoji}'


class Attachments(models.Model):
    task = models.ForeignKey(Task, related_name='attachments', on_delete=models.CASCADE)
    file = models.FileField(upload_to='tasks/attachments/')
    user = models.ForeignKey(BaseUser, related_name='attachments_of_task', on_delete=models.CASCADE)

    def __str__(self):
        return f'task={self.task.__str__()}::user={self.user.__str__()}::file={self.file}'
