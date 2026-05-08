import os
import shutil
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse
import replicate
from tempfile import NamedTemporaryFile

app = FastAPI()

# سيقوم الكود بجلب المفتاح من إعدادات Render (Environment Variables)
API_TOKEN = os.getenv("r8_4ElpchhTv09CVRhzkwlVOADZYQRg0Ny29IYEM")

@app.get("/", response_class=HTMLResponse)
async def main():
    if os.path.exists("templates/index.html"):
        with open("templates/index.html", "r", encoding="utf-8") as f:
            return f.read()
    return "File templates/index.html not found"

@app.post("/enhance-video")
async def enhance_video(
    file: UploadFile = File(...),
    scale: str = Form("2"),
    face_enhance: str = Form("false"),
    fps: str = Form("24")
):
    if not API_TOKEN:
        return {"error": "المفتاح غير موجود في إعدادات Render. يرجى إضافته في خانة Environment Variables باسم REPLICATE_API_TOKEN"}
    
    temp_path = None
    try:
        client = replicate.Client(api_token=API_TOKEN)
        suffix = os.path.splitext(file.filename)[1]
        with NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            shutil.copyfileobj(file.file, temp_file)
            temp_path = temp_file.name

        is_face_true = True if face_enhance.lower() == "true" else False
        
        with open(temp_path, "rb") as f:
            output = client.run(
                "lucataco/real-esrgan-video:de797303d73507301c2cf4a29a4358a9dfeb8c6c8c4a457a41ec59d0421e3305",
                input={
                    "video": f,
                    "upscale": int(scale),
                    "face_enhance": is_face_true,
                    "fps": int(fps)
                }
            )
        return {"video_url": str(output)}
    except Exception as e:
        return {"error": str(e)}
    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
