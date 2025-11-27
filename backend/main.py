from fastapi import APIRouter, FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from backend.app.ocr.parser import extract_text_and_info
from datetime import datetime
import os

app = FastAPI()
router = APIRouter(prefix="/api")

# 把 router 注册到 app
app.include_router(router)

# 上传图片保存路径
UPLOAD_FOLDER = "backend/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        # 保存图片
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{timestamp}_{file.filename}"
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # OCR + 信息抽取
        raw_text, structured = extract_text_and_info(file_path)

        return {
            "status": "success",
            "filename": filename,
            "path": file_path,
            "raw_text": raw_text,
            "structured": structured
        }

    except Exception as e:
        return JSONResponse({
            "status": "error",
            "message": str(e)
        }, status_code=500)
