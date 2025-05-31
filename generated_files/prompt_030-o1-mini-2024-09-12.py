from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
from typing import Optional, Union
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import base64

app = FastAPI()

class URLRequest(BaseModel):
    url: HttpUrl

class PreviewResponse(BaseModel):
    content_type: str
    preview: Optional[Union[str, dict]] = None

@app.post("/preview", response_model=PreviewResponse)
def get_preview(request: URLRequest):
    try:
        response = requests.get(request.url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        raise HTTPException(status_code=400, detail=str(e))

    content_type = response.headers.get('Content-Type', '').split(';')[0]

    if content_type == 'text/html':
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string if soup.title else 'No title'
        paragraphs = [p.get_text() for p in soup.find_all('p')][:2]
        preview = {
            "title": title,
            "summary": ' '.join(paragraphs)
        }
    elif content_type.startswith('image/'):
        try:
            image = Image.open(BytesIO(response.content))
            image.thumbnail((100, 100))
            buffer = BytesIO()
            image.save(buffer, format=image.format)
            img_str = base64.b64encode(buffer.getvalue()).decode()
            preview = f"data:{content_type};base64,{img_str}"
        except Exception as e:
            preview = "Unable to generate image preview."
    elif content_type == 'text/plain':
        lines = response.text.splitlines()[:5]
        preview = '\n'.join(lines)
    else:
        preview = f"Content type '{content_type}' is not supported for preview."

    return PreviewResponse(content_type=content_type, preview=preview)