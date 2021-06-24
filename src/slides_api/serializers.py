from rest_framework import serializers


class SlideFeaturesSerializer(serializers.Serializer):
    """Serializer for slide attributes"""
    max_slides = serializers.IntegerField(min_value=5, max_value=30)
    subject = serializers.CharField(max_length=255)
    language = serializers.ChoiceField(choices=['en', 'pt'])
