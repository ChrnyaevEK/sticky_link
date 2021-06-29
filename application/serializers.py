from rest_framework import serializers
from application import models
from django.contrib.auth.models import User


class ObjectSerializer(serializers.BaseSerializer):
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


class UserSerializer(CustomModelSerializer):
    type = serializers.ReadOnlyField()
    username = serializers.ReadOnlyField()
    email = serializers.ReadOnlyField()
    is_anonymous = serializers.ReadOnlyField()
    is_authenticated = serializers.ReadOnlyField()
    id = serializers.ReadOnlyField()

    class Meta:
        fields = ['type', 'username', 'email', 'is_anonymous', 'is_authenticated', 'id', 'trusted_walls']
        model = User


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
    trusted_users = UserSerializer(many=True, read_only=True)

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
    source = SourceSerializer(required=False)

    class Meta:
        fields = '__all__'
        model = models.Document


class Meta(serializers.Serializer):
    owner_permission = serializers.ReadOnlyField(default=False)
    trusted_permission = serializers.ReadOnlyField(default=False)
    anonymous_permission = serializers.ReadOnlyField(default=False)
    file_size_max = serializers.ReadOnlyField(default=10485760)
