from rest_framework import serializers
from application import models


class WallSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Wall
        fields = '__all__'


class SimpleTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SimpleText
        fields = '__all__'


class RichTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RichText
        fields = '__all__'


class URLSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.URL
        fields = '__all__'


class SimpleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SimpleList
        fields = '__all__'
