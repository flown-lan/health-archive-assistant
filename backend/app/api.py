# from fastapi import APIRouter, UploadFile
# from .ocr.parser import parse_image

# router = APIRouter(prefix="/api")

# @router.post("/ocr")
# async def ocr(file: UploadFile):
#     content = await file.read()
#     result = parse_image(content)
#     return {"result": result}


from fastapi import APIRouter, FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from .ocr.parser import parse_image
import os
from datetime import datetime

router = APIRouter(prefix="/api")

@router.post("/ocr")
async def ocr(file: UploadFile):
    content = await file.read()
    result = parse_image(content)
    return {"result": result}

app = FastAPI()

# 把 router 注册到 app
app.include_router(router)

# 上传图片保存路径
UPLOAD_FOLDER = "backend/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        # 构建保存文件名，避免重名
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{timestamp}_{file.filename}"
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        
        # 保存文件到本地
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        return JSONResponse({
            "status": "success",
            "filename": filename,
            "path": file_path
        })
    except Exception as e:
        return JSONResponse({
            "status": "error",
            "message": str(e)
        }, status_code=500)
