import os
import io
import re
import time
import logging
from PIL import Image
from paddleocr import PaddleOCR
from concurrent.futures import ProcessPoolExecutor

# 导入你即将创建的预处理模块
from .preprocess import preprocess_image

logging.basicConfig(level=logging.INFO)
ocr = None


def get_ocr():
    """使用轻量级移动端模型（显式指定模型名称）"""
    global ocr
    if ocr is None:
        base = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "models", "paddleocr"))
        det_dir = os.path.join(base, "ch_PP-OCRv4_det_mobile")
        rec_dir = os.path.join(base, "ch_PP-OCRv4_rec_mobile")
        
        logging.info(f"det_model_dir: {det_dir}, exists: {os.path.exists(det_dir)}")
        logging.info(f"rec_model_dir: {rec_dir}, exists: {os.path.exists(rec_dir)}")
        
        ocr = PaddleOCR(
            text_detection_model_name='PP-OCRv4_mobile_det',
            text_detection_model_dir=det_dir,
            text_recognition_model_name='PP-OCRv4_mobile_rec',
            text_recognition_model_dir=rec_dir,
            use_textline_orientation=False,
            # 关键：禁用文档矫正（UVDoc 很慢，速度提升 50%+）
            use_doc_unwarping=False
        )
        logging.info("PaddleOCR initialized (mobile models, fast mode).")
    return ocr


def extract_text_and_info(image_path: str):
    """本地模型 OCR + 文本结构化处理（包含图片预处理）"""
    try:
        # --- 预处理图像 ---
        processed_img = preprocess_image(image_path)

        # --- OCR ---
        ocr_instance = get_ocr()
        start = time.time()
        result = ocr_instance.ocr(processed_img)
        logging.info(f"OCR inference time: {time.time() - start:.2f}s")

    except Exception as e:
        logging.exception("OCR failed")
        return "", {"name": "", "date": "", "hospital": "", "type": ""}

    # 解析 OCR 返回
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

    # -------- 结构化抽取 --------
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
    """直接处理上传的图片（二进制流）"""
    try:
        # 将 bytes 转为 PIL Image
        image = Image.open(io.BytesIO(image_content)).convert("RGB")

        # 将 PIL Image 交给 preprocess
        processed_img = preprocess_image(image)

        ocr_instance = get_ocr()
        result = ocr_instance.ocr(processed_img)
        return {"status": "success", "raw": result}

    except Exception as e:
        logging.exception("parse_image failed")
        return {"status": "error", "message": str(e)}


def extract_text_and_info_batch(image_paths: list):
    """批量处理多张图片"""
    with ProcessPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(extract_text_and_info, image_paths))
    return results
