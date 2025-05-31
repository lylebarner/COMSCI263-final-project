from django.http import StreamingHttpResponse, Http404
from django.views import View
import os

class StreamMediaView(View):
    def get(self, request, filename):
        media_root = os.path.join(os.path.dirname(__file__), 'media')  # Update to your media directory
        file_path = os.path.join(media_root, filename)

        if not os.path.exists(file_path):
            raise Http404("File not found")

        def file_iterator(file_name, chunk_size=1024):
            with open(file_name, 'rb') as file:
                while chunk := file.read(chunk_size):
                    yield chunk

        response = StreamingHttpResponse(file_iterator(file_path))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        return response

# In your urls.py
from django.urls import path
from .views import StreamMediaView

urlpatterns = [
    path('stream/<str:filename>/', StreamMediaView.as_view(), name='stream_media'),
]