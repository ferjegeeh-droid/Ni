import os
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse
import replicate

app = FastAPI()

# ضع التوكن هنا أو في إعدادات Render كـ Environment Variable باسم REPLICATE_API_TOKEN
os.environ["REPLICATE_API_TOKEN"] = "ضع_هنا_مفتاح_API_الخاص_بك"

@app.get("/", response_class=HTMLResponse)
async def main():
    with open("templates/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/enhance")
async def enhance_image(file: UploadFile = File(...)):
    # رفع الصورة مؤقتاً أو إرسالها كـ Byte
    # موديل Real-ESRGAN على Replicate
    input_data = {"image": file.file}
    
    try:
        output = replicate.run(
            "xinntao/realesrgan:1b97c3c68525c7645ee3611f79616521996e7af63f133b3ca2f0e05f628c899c",
            input=input_data
        )
        # output سيكون رابط الصورة المحسنة جاهزة
        return {"url": output}
    except Exception as e:
        return {"error": str(e)}
