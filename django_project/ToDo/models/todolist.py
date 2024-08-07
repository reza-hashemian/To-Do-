import uuid

from django.db import models
from django.utils import timezone

from django_project.common.models import BaseModel
from django_project.users.models import BaseUser

from .boards import Board


class ToDoList(BaseModel):
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

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    priority = models.PositiveSmallIntegerField(default=0)
    color = models.CharField(max_length=30, default=ColorChoice.CYAN,
                             choices=ColorChoice.choices)
    board = models.ForeignKey(Board, on_delete=models.CASCADE,
                              related_name='todolists', related_query_name='todolist')



    class Meta:
        unique_together = ('name', 'board')
        ordering = ['-priority', 'created_at']

    def __str__(self):
        return f"{self.name}>>{self.board.__str__()}"


