import os
import io
import re
import time
import logging
from PIL import Image
from paddleocr import PaddleOCR

logging.basicConfig(level=logging.INFO)
ocr = None

def get_ocr():
    """使用本地检测模型 + 本地识别模型"""
    global ocr
    if ocr is None:
        base = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "models", "paddleocr"))
        det_dir = os.path.join(base, "PP-OCRv5_server_det")  # 软链到 ch_PP-OCRv4_det_infer
        rec_dir = os.path.join(base, "PP-OCRv5_server_rec")  # 刚复制的本地识别模型
        logging.info(f"det_model_dir: {det_dir}, exists: {os.path.exists(det_dir)}")
        logging.info(f"rec_model_dir: {rec_dir}, exists: {os.path.exists(rec_dir)}")

        ocr = PaddleOCR(
            lang='ch',
            text_detection_model_dir=det_dir,
            text_recognition_model_dir=rec_dir,
            use_textline_orientation=False
        )
        logging.info("PaddleOCR initialized (local det + local rec).")
    return ocr

def extract_text_and_info(image_path: str):
    try:
        ocr_instance = get_ocr()
        start = time.time()
        result = ocr_instance.ocr(image_path)
        logging.info(f"OCR inference time: {time.time() - start:.2f}s")
    except Exception as e:
        logging.exception("OCR failed")
        return "", {"name": "", "date": "", "hospital": "", "type": ""}

    # 解析结果
    text_lines = []
    if isinstance(result, list) and len(result) > 0:
        first = result[0]
        if isinstance(first, dict) and 'rec_texts' in first:
            text_lines = first['rec_texts']
        elif isinstance(first, list):
            for block in result:
                for line in block:
                    try:
                        text_lines.append(line[1][0])
                    except Exception:
                        continue
    full_text = "\n".join(text_lines)

    # 简单结构化
    name_match = re.search(r"姓名[:：\s]*([\u4e00-\u9fa5·]{2,6})", full_text)
    date_match = re.search(r"(\d{4}[年/-]\d{1,2}[月/-]\d{1,2}[日号]?)", full_text)
    hospital_match = re.search(r"([\u4e00-\u9fa50-9（）()·\-A-Za-z]+(?:医院|中心|门诊|院区))", full_text)

    doc_type = "病历"
    if "检验" in full_text or "化验" in full_text:
        doc_type = "检验报告"
    elif any(x in full_text for x in ["影像", "放射", "CT", "MRI", "超声"]):
        doc_type = "影像检查"
    elif "报告" in full_text:
        doc_type = "报告"
    elif "门诊" in full_text:
        doc_type = "门诊病历"

    structured = {
        "name": name_match.group(1) if name_match else "",
        "date": date_match.group(1) if date_match else "",
        "hospital": hospital_match.group(1) if hospital_match else "",
        "type": doc_type
    }
    return full_text, structured

def parse_image(image_content: bytes):
    try:
        image = Image.open(io.BytesIO(image_content)).convert("RGB")
        ocr_instance = get_ocr()
        result = ocr_instance.ocr(image)
        return {"status": "success", "raw": result}
    except Exception as e:
        logging.exception("parse_image failed")
        return {"status": "error", "message": str(e)}