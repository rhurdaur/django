from rest_framework import serializers
from events.models import Category, Event, Review


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        exclude = ("author", "event")


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        exclude = ("author",)


class EventInlineSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()  # nutzt String-Repräsentation

    class Meta:
        model = Event
        fields = ("id", "name", "date", "author")


class EventSerializer(serializers.ModelSerializer):

    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Event
        fields = ("id", "name", "date", "author", "reviews", "sub_title")


class EventCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        exclude = ("author", "id", "is_active")

    def validate_name(self, value):
        if "xxxx" in value:
            raise serializers.ValidationError()
        return value


class CategorySerializer(serializers.ModelSerializer):

    events = EventInlineSerializer(read_only=True, many=True)

    class Meta:
        model = Category
        fields = (
            "name",
            "sub_title",
            "description",
            "events",
        )


class SimpleSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=30)
    age = serializers.IntegerField()
