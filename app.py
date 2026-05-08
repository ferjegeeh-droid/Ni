import os
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse
import replicate
import uvicorn

app = FastAPI()

# تأكد من وضع التوكن في إعدادات Render كما فعلنا سابقاً
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")

@app.get("/", response_class=HTMLResponse)
async def main():
    with open("templates/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/enhance-video")
async def enhance_video(
    file: UploadFile = File(...),
    scale: int = Form(2), # التكبير (2x أو 4x)
    face_enhance: bool = Form(False), # تحسين الوجوه
    fps: int = Form(24) # عدد الفريمات
):
    try:
        # استخدام موديل Real-ESRGAN للفيديو
        output = replicate.run(
            "lucataco/real-esrgan-video:de797303d73507301c2cf4a29a4358a9dfeb8c6c8c4a457a41ec59d0421e3305",
            input={
                "video": file.file,
                "upscale": scale,
                "face_enhance": face_enhance,
                "fps": fps
            }
        )
        # النتيجة تكون رابط فيديو MP4 عالي الجودة
        return {"video_url": output}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)
