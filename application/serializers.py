from rest_framework import serializers
from application import models
from django.contrib.auth.models import User


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


class UserSerializer(serializers.ModelSerializer):
    def get_queryset(self):
        return models.User.objects.filter(pk=self.request.user.id)

    class Meta:
        model = User
        fields = ['username', 'email', 'id']


class SimpleTextSerializer(serializers.ModelSerializer):
    type = serializers.ReadOnlyField(default=models.SimpleText.type)

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


class CounterSerializer(serializers.ModelSerializer):
    type = serializers.ReadOnlyField(default=models.Counter.type)

    class Meta:
        model = models.Counter
        fields = '__all__'


class WallSerializer(serializers.ModelSerializer):
    type = serializers.ReadOnlyField(default=models.Wall.type)
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
        model = models.Wall
        fields = '__all__'
