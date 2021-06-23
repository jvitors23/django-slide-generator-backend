from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import SlideAttributesSerializer


class SlidesAPIView(APIView):
    """Slides API - Given slide features (subject, topics, sources) returns the slide images and texts"""

    serializer_class = SlideAttributesSerializer

    def post(self, request):
        """Given topics return slide images and text"""

        # Get text from wikipedia
        # Clean text
        # Download Images
        serializer = SlideAttributesSerializer(data=request.data)
        if serializer.is_valid():
            slide_features = serializer.validated_data

            return Response(slide_features)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
