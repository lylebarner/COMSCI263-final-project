# views.py
import os
from django.conf import settings
from django.http import FileResponse, Http404
from django.views import View

class StreamMediaView(View):
    def get(self, request, filename):
        # Prevent directory traversal
        if '..' in filename or filename.startswith('/'):
            raise Http404("Invalid file path.")

        file_path = os.path.join(settings.MEDIA_ROOT, filename)

        if not os.path.exists(file_path) or not os.path.isfile(file_path):
            raise Http404("File does not exist.")

        return FileResponse(open(file_path, 'rb'), as_attachment=False)

# urls.py
from django.urls import path
from .views import StreamMediaView

urlpatterns = [
    path('api/stream/<str:filename>/', StreamMediaView.as_view(), name='stream_media'),
]