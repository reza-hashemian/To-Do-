import uuid

from django.db import models

from django_project.common.models import BaseModel
from django_project.users.models import BaseUser


class Board(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    baseuser = models.ForeignKey(BaseUser, on_delete=models.CASCADE,
                                    related_name='boards', related_query_name='board_obj')

    class Meta:
        unique_together = ('baseuser', 'name')

    def __str__(self):
        return f'{self.name}>>{self.baseuser.__str__()}'

