from rest_framework.response import Response
from rest_framework.views import APIView


class SlidesAPIView(APIView):
    """Slides API"""

    def post(self, request):
        """Given topics return slide images and text"""

        # Get text from wikipedia
        # Clean text
        # Download Images

        return Response(request.data)
