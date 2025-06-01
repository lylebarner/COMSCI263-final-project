# views.py
import mimetypes
import os
from django.conf import settings
from django.http import FileResponse, Http404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class StreamMediaFile(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, filename):
        # Assuming media files are in settings.MEDIA_ROOT
        file_path = os.path.join(settings.MEDIA_ROOT, filename)
        if not os.path.exists(file_path):
            raise Http404("File does not exist.")

        mime_type, _ = mimetypes.guess_type(file_path)
        response = FileResponse(open(file_path, "rb"), content_type=mime_type)
        response["Content-Disposition"] = f'inline; filename="{filename}"'
        return response

# urls.py
from django.urls import path
from .views import StreamMediaFile

urlpatterns = [
    path('api/media/stream/<str:filename>/', StreamMediaFile.as_view(), name='stream-media-file'),
]
```