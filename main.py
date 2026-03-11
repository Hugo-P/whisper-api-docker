# Whisper FastAPI 服務
from fastapi import FastAPI, File, UploadFile, HTTPException
import whisper
import tempfile
import os

app = FastAPI(title="Whisper API", description="OpenAI Whisper 語音識別 API")

# 模型緩存
model = None

def get_model():
    """加載 Whisper 模型"""
    global model
    if model is None:
        model = whisper.load_model("tiny")
    return model

@app.get("/")
async def root():
    """根路徑，返回服務資訊"""
    return {
        "service": "Whisper API",
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/health")
async def health():
    """健康檢查"""
    return {"status": "healthy"}

@app.post("/asr")
async def asr(file: UploadFile = File(...)):
    """
    語音識別 API

    參數：
        file: 音頻文件（支持 mp3, wav, m4a 等）

    返回：
        {"text": "識別到的文字"}
    """
    try:
        # 加載模型
        model = get_model()

        # 保存臨時文件
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name

        # 識別語音
        result = model.transcribe(tmp_path)

        # 清除臨時文件
        os.unlink(tmp_path)

        return {"text": result["text"]}

    except Exception as e:
        # 如果有錯誤，確保刪除臨時文件
        if 'tmp_path' in locals() and os.path.exists(tmp_path):
            os.unlink(tmp_path)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/asr/{language}")
async def asr_with_language(language: str, file: UploadFile = File(...)):
    """
    指定語言的語音識別 API

    參數：
        language: 語言代碼（如 zh, en, ja）
        file: 音頻文件

    返回：
        {"text": "識別到的文字"}
    """
    try:
        # 加載模型
        model = get_model()

        # 保存臨時文件
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name

        # 識別語音（指定語言）
        result = model.transcribe(tmp_path, language=language)

        # 清除臨時文件
        os.unlink(tmp_path)

        return {"text": result["text"]}

    except Exception as e:
        if 'tmp_path' in locals() and os.path.exists(tmp_path):
            os.unlink(tmp_path)
        raise HTTPException(status_code=500, detail=str(e))
