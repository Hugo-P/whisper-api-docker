# 為了構建 whisper API 服務的 Dockerfile
FROM python:3.11-slim

# 安裝系統依賴
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# 安裝 Python 套件
RUN pip install --no-cache-dir \
    openai-whisper \
    fastapi \
    uvicorn \
    python-multipart

# 設定工作目錄
WORKDIR /app

# 複製 API 代碼
COPY main.py .

# 暴露端口
EXPOSE 9000

# 啟動 API 服務
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000"]
