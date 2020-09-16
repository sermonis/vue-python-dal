from rest_framework import serializers

from dms.models import (
    Author,
    Document,
    Category,
    Publisher,
    Subject,
)


class AuthorSerializer(serializers.ModelSerializer):
    """Serializes Author model."""

    class Meta:
        model = Author
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    """Serializes Category model."""

    class Meta:
        model = Category
        fields = "__all__"


class PublisherSerializer(serializers.ModelSerializer):
    """Serializes Publisher model."""

    class Meta:
        model = Publisher
        fields = "__all__"


class SubjectSerializer(serializers.ModelSerializer):
    """Serializes Subject model."""

    class Meta:
        model = Subject
        fields = "__all__"


class TagListField(serializers.ListField):
    child = serializers.CharField()

    def to_representation(self, data):
        return data.values_list("name", flat=True)


class DocumentSerializer(serializers.ModelSerializer):
    """Serializes Document model."""

    tags = TagListField(required=False)

    class Meta:
        model = Document
        fields = "__all__"

    def create(self, validated_data):
        tags = validated_data.pop("tags", None)
        instance = super().create(validated_data)
        if tags:
            instance.tags.set(*tags)
        return instance

    def update(self, instance, validated_data):
        tags = validated_data.pop("tags", None)
        instance = super().update(instance, validated_data)
        if tags:
            instance.tags.set(*tags, clear=True)
        return instance
