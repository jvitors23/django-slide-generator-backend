from rest_framework import serializers


class SlideFeaturesSerializer(serializers.Serializer):
    """Serializer for slide attributes"""
    max_slides = serializers.IntegerField(min_value=5, max_value=30,
                                          help_text='Max number of slides '
                                                    'considering '
                                                    'introduction and '
                                                    'references')
    subject = serializers.CharField(max_length=255, help_text='Slide subject')
    language = serializers.ChoiceField(choices=['en', 'pt'],
                                       help_text="Slide language, current "
                                                 "supported languages: [en, "
                                                 "pt]")
