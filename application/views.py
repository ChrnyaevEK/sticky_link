from application.models import SimpleText
from application.serializers import SimpleTextSerializer
from rest_framework import viewsets


class SimpleTextViewSet(viewsets.ModelViewSet):
    queryset = SimpleText.objects.all()
    serializer_class = SimpleTextSerializer
