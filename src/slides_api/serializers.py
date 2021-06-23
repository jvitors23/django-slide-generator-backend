from rest_framework import serializers


class SlideAttributesSerializer(serializers.Serializer):
    """Serializer for slide attributes"""
    num_slides = serializers.IntegerField()
    subject = serializers.CharField(max_length=255)
    topics = serializers.ListField(child=serializers.CharField(max_length=255))
    sources = serializers.ListField(child=serializers.URLField(), required=False)

