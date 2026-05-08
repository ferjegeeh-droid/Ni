from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
import cv2
from basicsr.archs.rrdbnet_arch import RRDBNet
from realesrgan import RealESRGANer
import numpy as np

app = FastAPI()

# إعداد نموذج الذكاء الاصطناعي (نسخة خفيفة لتناسب سيرفرات Render)
model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4)
upsampler = RealESRGANer(
    scale=4,
    model_path='https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth',
    model=model,
    tile=0,
    tile_pad=10,
    pre_pad=0,
    half=False # Render لا يدعم Half precision بدون GPU
)

@app.get("/", response_class=HTMLResponse)
async def main():
    with open("templates/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/enhance")
async def enhance_image(file: UploadFile = File(...)):
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # عملية التحسين (هنا يحدث السحر)
    output, _ = upsampler.enhance(img, outscale=4)
    
    output_path = "enhanced_image.png"
    cv2.imwrite(output_path, output)
    
    return FileResponse(output_path)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)
