FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# تحميل الأوزان مسبقاً لتسريع التشغيل
RUN python -c "from basicsr.archs.rrdbnet_arch import RRDBNet; from realesrgan import RealESRGANer; RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4)"

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "10000"]
