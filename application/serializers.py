from rest_framework import serializers
from application import models


class WallSerializer(serializers.ModelSerializer):
    type = serializers.ReadOnlyField(default=models.Wall.type)

    class Meta:
        model = models.Wall
        fields = '__all__'


class SimpleTextSerializer(serializers.ModelSerializer):
    type = serializers.ReadOnlyField(default=models.SimpleText.type)
    max_length = serializers.ReadOnlyField(default=models.SimpleText.max_length)

    class Meta:
        model = models.SimpleText
        fields = '__all__'


class RichTextSerializer(serializers.ModelSerializer):
    type = serializers.ReadOnlyField(default=models.RichText.type)

    class Meta:
        model = models.RichText
        fields = '__all__'


class URLSerializer(serializers.ModelSerializer):
    type = serializers.ReadOnlyField(default=models.URL.type)

    class Meta:
        model = models.URL
        fields = '__all__'


class SimpleListSerializer(serializers.ModelSerializer):
    type = serializers.ReadOnlyField(default=models.SimpleList.type)

    class Meta:
        model = models.SimpleList
        fields = '__all__'
