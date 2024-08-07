from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet
from drf_spectacular.utils import extend_schema
from django_project.api.mixins import ApiAuthMixin

from ..models.boards import Board


@extend_schema(tags=['Board'])
class BoardViewSetAPI(ApiAuthMixin, ModelViewSet):
    class BoardSerializer(ModelSerializer):
        class Meta:
            model = Board
            fields = ['id', 'name', 'description']
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

    def list(self, request, *args, **kwargs):
        return Response(self.BoardSerializer(self.get_queryset().filter(baseuser=request.user), many=True).data)

    def perform_create(self, serializer):
        serializer.save(baseuser=self.request.user)



