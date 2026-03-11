# Whisper API Docker 服務

這個目錄包含自建 Whisper API 的 Docker 配置。

## 文件結構

```
whisper/
├── Dockerfile    # Docker 映像定義
├── main.py      # FastAPI 應用
└── README.md    # 這個文件
```

## 構建和運行

### 方式一：使用 GitHub Container Registry 映像（推薦）

```bash
docker run -d \
  --name whisper \
  -p 9000:9000 \
  --restart unless-stopped \
  ghcr.io/Hugo-P/whisper-api-docker:latest
```

### 方式二：使用 docker-compose

1. 更新 docker-compose.yml：

```yaml
whisper:
  image: ghcr.io/Hugo-P/whisper-api-docker:latest
  container_name: whisper
  restart: unless-stopped
  ports:
    - "9000:9000"
  shm_size: 1gb
```

2. 啟動服務：

```bash
docker-compose up -d whisper
```

### 方式三：自行建構

```bash
docker build -t whisper-api .
docker run -d -p 9000:9000 --name whisper whisper-api
```

3. 測試 API：

```bash
# 健康檢查
curl http://localhost:9000/health

# 語音識別
curl -X POST http://localhost:9000/asr \
  -H "Content-Type: multipart/form-data" \
  -F "file=@test.mp3"
```

## API 端點

### `GET /`
返回服務資訊

### `GET /health`
健康檢查

### `POST /asr`
語音識別（自動偵測語言）
- 參數：`file`（音頻文件）
- 返回：`{"text": "識別文字"}`

### `POST /asr/{language}`
指定語言的語音識別
- 參數：`language`（語言代碼）、`file`
- 返回：`{"text": "識別文字"}`

## 支持的語言代碼

- `zh` - 中文
- `en` - 英文
- `ja` - 日文
- `ko` - 韓文
- 等等...

## Dockerfile 說明

- 基礎映像：`python:3.11-slim`
- 系統套件：`ffmpeg`
- Python 套件：
  - `openai-whisper`
  - `fastapi`
  - `uvicorn`
  - `python-multipart`

## 模型

默認使用 `tiny` 模型（最快，大小最小）。

如需更改模型，修改 `main.py`：

```python
model = whisper.load_model("tiny")  # 可改成 base, small, medium, large
```

## GitHub Actions 自動建構

此專案使用 GitHub Actions 自動建構並推送 Docker 映像到 GitHub Container Registry (ghcr.io)。

### 設定步驟

1. 在 GitHub Repository 中啟用 Packages：
   - 前往 Settings → Actions → General
   - 在 "Workflow permissions" 選擇 "Read and write permissions"

2. 推送程式碼到 `main` 或 `master` 分支，GitHub Actions 會自動：
   - 建構 Docker 映像
   - 推送到 GitHub Container Registry (ghcr.io)
   - 自動標記版本（latest、分支名稱、commit SHA）

**注意：** 不需要額外設定 Secrets，GitHub Actions 會自動使用 `GITHUB_TOKEN` 進行認證。

### 手動觸發建構

您可以透過以下方式手動觸發建構：

**方式一：透過 GitHub 網頁介面**
1. 前往 Actions 頁面：https://github.com/Hugo-P/whisper-api-docker/actions
2. 選擇 "Build and Push Docker Image" workflow
3. 點擊 "Run workflow" 按鈕
4. 選擇分支並點擊 "Run workflow"

**方式二：透過 Git 推送**
```bash
git push origin main
```

### 從 GitHub Container Registry 拉取映像

```bash
docker pull ghcr.io/Hugo-P/whisper-api-docker:latest
```

## 授權

本專案使用 MIT 授權。詳見 [LICENSE](LICENSE) 檔案。
