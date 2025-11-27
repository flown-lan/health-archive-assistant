from fastapi import APIRouter, UploadFile
from .ocr.parser import parse_image

router = APIRouter(prefix="/api")

@router.post("/ocr")
async def ocr(file: UploadFile):
    content = await file.read()
    result = parse_image(content)
    return {"result": result}
