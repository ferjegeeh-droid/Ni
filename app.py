import os
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
import replicate
import uvicorn

app = FastAPI()

# سيقوم البرنامج بالبحث عن المفتاح في إعدادات السيرفر تلقائياً
# REPLICATE_API_TOKEN يجب أن يكون معرفاً في Render

@app.get("/", response_class=HTMLResponse)
async def main():
    if os.path.exists("templates/index.html"):
        with open("templates/index.html", "r", encoding="utf-8") as f:
            return f.read()
    return "File templates/index.html not found"

@app.post("/enhance")
async def enhance_image(file: UploadFile = File(...)):
    try:
        # استخدام موديل Real-ESRGAN
        output = replicate.run(
            "xinntao/realesrgan:1b97c3c68525c7645ee3611f79616521996e7af63f133b3ca2f0e05f628c899c",
            input={"image": file.file}
        )
        return {"url": output}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)
