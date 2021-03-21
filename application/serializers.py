from rest_framework import serializers
from application import models
from django.contrib.auth.models import User
from application.utils import get_version_hash
from django.core.exceptions import PermissionDenied


class ObjectSerializer(serializers.BaseSerializer):
    """
    A read-only serializer that coerces arbitrary complex objects
    into primitive representations.
    """

    def to_representation(self, instance):
        if isinstance(instance, (list, set, tuple)):
            return [
                self.to_representation(item) for item in instance
            ]
        elif isinstance(instance, (str, int, bool, float, type(None))):
            return instance
        else:
            output = {}
            for attribute_name in dir(instance):
                attribute = getattr(instance, attribute_name)
                if attribute_name.startswith('_'):
                    # Ignore private attributes.
                    pass
                elif hasattr(attribute, '__class__'):
                    output[attribute_name] = self.to_representation(attribute)
                elif hasattr(attribute, '__call__'):
                    # Ignore methods and other callables.
                    pass
                elif isinstance(attribute, (str, int, bool, float, type(None))):
                    # Primitive types can be passed through unmodified.
                    output[attribute_name] = attribute
                elif isinstance(attribute, list):
                    # Recursively deal with items in lists.
                    output[attribute_name] = [
                        self.to_representation(item) for item in attribute
                    ]
                elif isinstance(attribute, dict):
                    # Recursively deal with items in dictionaries.
                    output[attribute_name] = {
                        str(key): self.to_representation(value)
                        for key, value in attribute.items()
                    }
                else:
                    # Force anything else to its string representation.
                    output[attribute_name] = str(attribute)
            return output


class CustomModelSerializer(serializers.ModelSerializer):
    type = serializers.ReadOnlyField()
    uid = serializers.ReadOnlyField()

    def to_representation(self, instance):
        """Add version hash"""
        representation = super().to_representation(instance)
        representation['version'] = get_version_hash(representation)
        return representation

    def update(self, instance, validated_data):
        owner = instance.owner if instance.type == models.Wall.type else instance.wall.owner
        user = self.context['request'].user
        if user.is_anonymous or owner != user:  # Check if no protected fields are to be updated
            protected_fields = models.Wall.Default.protected_fields if instance.type == models.Wall.type else models.Widget.Default.protected_fields
            if set(protected_fields).intersection(validated_data.keys()):
                raise PermissionDenied()
        return super().update(instance, validated_data)


class UserSerializer(CustomModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'is_anonymous', 'is_authenticated']


class SimpleTextSerializer(CustomModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.SimpleText


class URLSerializer(CustomModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.URL


class SimpleListSerializer(CustomModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.SimpleList


class CounterSerializer(CustomModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.Counter


class SimpleSwitchSerializer(CustomModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.SimpleSwitch


class WallSerializer(CustomModelSerializer):
    widgets = [
        SimpleTextSerializer(many=True, read_only=True),
        URLSerializer(many=True, read_only=True),
        CounterSerializer(many=True, read_only=True),
        SimpleListSerializer(many=True, read_only=True),
    ]
    owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = '__all__'
        model = models.Wall
