from rest_framework import serializers
from application import models
from django.contrib.auth.models import User
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
    id = serializers.ReadOnlyField()
    version = serializers.ReadOnlyField()
    date_of_creation = serializers.ReadOnlyField()
    last_update = serializers.ReadOnlyField()

    def update(self, instance, validated_data):
        user = self.context['request'].user
        owner = instance.related_wall_instance.owner

        if (user.is_anonymous or user != owner) and not instance.validate_anonymous_access(validated_data.keys()):
            raise PermissionDenied()  # User has no right to change any of accessed fields

        return super().update(instance, validated_data)


class UserSerializer(CustomModelSerializer):
    type = serializers.ReadOnlyField(default='user')

    class Meta:
        model = User
        fields = ['username', 'email', 'is_anonymous', 'is_authenticated']


class CustomWidgetSerializer(CustomModelSerializer):
    is_referenced = serializers.ReadOnlyField()
    pass


class SimpleTextSerializer(CustomWidgetSerializer):
    class Meta:
        fields = '__all__'
        model = models.SimpleText


class URLSerializer(CustomWidgetSerializer):
    class Meta:
        fields = '__all__'
        model = models.URL


class SimpleListSerializer(CustomWidgetSerializer):
    class Meta:
        fields = '__all__'
        model = models.SimpleList


class CounterSerializer(CustomWidgetSerializer):
    class Meta:
        fields = '__all__'
        model = models.Counter


class SimpleSwitchSerializer(CustomWidgetSerializer):
    class Meta:
        fields = '__all__'
        model = models.SimpleSwitch


class ContainerSerializer(CustomModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.Container


class WallSerializer(CustomModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.Wall


class PortSerializer(CustomModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.Port


class SourceSerializer(CustomModelSerializer):
    name = serializers.ReadOnlyField()

    class Meta:
        fields = '__all__'
        model = models.Source


class DocumentSerializer(CustomModelSerializer):
    source = SourceSerializer()

    class Meta:
        fields = '__all__'
        model = models.Document
