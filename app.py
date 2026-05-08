import os
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse
import replicate
import uvicorn

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def main():
    with open("templates/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/enhance-video")
async def enhance_video(
    file: UploadFile = File(...),
    scale: str = Form("2"),
    face_enhance: str = Form("false"),
    fps: str = Form("24")
):
    try:
        # تحويل القيم لنوع البيانات الصحيح
        is_face_true = True if face_enhance.lower() == "true" else False
        scale_int = int(scale)
        fps_int = int(fps)

        # تشغيل الموديل باستخدام رابط مباشر للملف المؤقت
        output = replicate.run(
            "lucataco/real-esrgan-video:de797303d73507301c2cf4a29a4358a9dfeb8c6c8c4a457a41ec59d0421e3305",
            input={
                "video": file.file, # إرسال الملف كـ stream
                "upscale": scale_int,
                "face_enhance": is_face_true,
                "fps": fps_int
            }
        )
        return {"video_url": str(output)}
    except Exception as e:
        # التأكد من إرسال الخطأ كنص فقط لتجنب مشكلة الـ JSON
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)
