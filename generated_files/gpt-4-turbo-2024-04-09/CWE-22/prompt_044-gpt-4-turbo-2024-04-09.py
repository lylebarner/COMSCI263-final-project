from django.http import StreamingHttpResponse
from django.views import View
import os

class StreamMediaView(View):
    def get(self, request, filename):
        # Define the path to media files
        media_path = "/path/to/your/media/files"
        file_path = os.path.join(media_path, filename)

        # Ensure the file exists to prevent path traversal attacks
        if os.path.exists(file_path) and os.path.isfile(file_path) and os.path.realpath(file_path).startswith(media_path):
            # Stream the file in chunks to handle large files
            def file_iterator(file_name, chunk_size=8192):
                with open(file_name, mode='rb') as f:
                    while True:
                        data = f.read(chunk_size)
                        if not data:
                            break
                        yield data
            
            response = StreamingHttpResponse(file_iterator(file_path))
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
        else:
            # Return 404 if file does not exist or attempts to access outside the media directory
            return HttpResponseNotFound("File not found.")

# In urls.py
# path('stream-media/<str:filename>/', StreamMediaView.as_view(), name='stream-media'),