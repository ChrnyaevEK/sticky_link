from rest_framework import serializers
from application.models import SimpleText


class SimpleTextSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SimpleText
        fields = '__all__'
