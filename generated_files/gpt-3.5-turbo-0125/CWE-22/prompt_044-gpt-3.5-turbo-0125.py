from django.http import FileResponse
from django.views.generic import View
from django.conf import settings
import os

class MediaStreamView(View):
    def get(self, request, filename):
        media_file_path = os.path.join(settings.MEDIA_ROOT, filename)
        if os.path.exists(media_file_path):
            return FileResponse(open(media_file_path, 'rb'), content_type='application/octet-stream')
        else:
            return HttpResponse(status=404)