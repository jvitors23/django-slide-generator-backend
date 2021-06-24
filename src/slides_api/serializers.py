from rest_framework import serializers


class SlideFeaturesSerializer(serializers.Serializer):
    """Serializer for slide attributes"""
    num_slides = serializers.IntegerField(min_value=5, max_value=20)
    subject = serializers.CharField(max_length=255)
    language = serializers.CharField(max_length=255)
    # topics = serializers.ListField(child=serializers.CharField(max_length=255))
    # sources = serializers.ListField(child=serializers.URLField(),
    #                                 required=False)
