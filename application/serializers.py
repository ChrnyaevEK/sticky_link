from rest_framework import serializers
from application import models
from django.contrib.auth.models import User
from application.utils import get_version_hash


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
        if self.context['request'].user.is_anonymous:  # Check if no protected fields are to be updated
            if set(instance.Default.protected_fields).intersection(validated_data.keys):
                raise serializers.ValidationError()
        return super().update(instance, validated_data)


class UserSerializer(CustomModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email']


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
