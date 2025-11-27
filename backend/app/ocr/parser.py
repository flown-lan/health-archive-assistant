from paddleocr import PaddleOCR
import re
import os
import logging
import time
import json

logging.basicConfig(level=logging.DEBUG)

# 延迟初始化 OCR（避免启动时卡住）
ocr = None

def get_ocr():
    """获取 OCR 实例，首次调用时初始化（强制使用官方模型，不读本地）"""
    global ocr
    if ocr is None:
        ocr = PaddleOCR(use_angle_cls=False, lang='ch')
        logging.debug("PaddleOCR initialized with official models")
    return ocr


def parse_image(image_content: bytes):
    """
    将图片字节内容进行 OCR 识别
    增加: 调试模式、PIL/Path 双策略、异常更详细
    """
    import io
    from PIL import Image

    try:
        # 转成 PIL 图片
        image = Image.open(io.BytesIO(image_content)).convert("RGB")

        # -------- 调试模式：仅当设置 OCR_DEBUG=1 时才写入临时文件 --------
        debug_path = None
        if os.environ.get("OCR_DEBUG") == "1":
            ts = int(time.time() * 1000)
            debug_path = f"/tmp/ocr_debug_{ts}.jpg"
            try:
                image.save(debug_path)
                logging.debug(f"[DEBUG] Saved debug image to: {debug_path}")
            except Exception:
                logging.exception("save debug image failed")
                debug_path = None

        ocr_instance = get_ocr()

        # -------- 优先采用 PIL 输入 --------
        raw_results = {"from_pil": None, "from_path": None}

        try:
            pil_result = ocr_instance.ocr(image)
            if pil_result and len(pil_result) > 0:
                raw_results["from_pil"] = pil_result
        except Exception:
            logging.exception("OCR from PIL failed")

        # -------- 若 PIL 有结果，则不再执行 path 模式 --------
        if raw_results["from_pil"] is None and debug_path:
            try:
                raw_results["from_path"] = ocr_instance.ocr(debug_path)
            except Exception:
                logging.exception("OCR from path failed")

        # -------- 保存完整调试结果 --------
        try:
            dbg_out = os.path.join(os.getcwd(), "backend", "ocr_raw_debug.json")
            with open(dbg_out, "w", encoding="utf-8") as fh:
                json.dump(raw_results, fh, ensure_ascii=False, indent=2)
            logging.debug(f"Wrote OCR raw results to: {dbg_out}")
        except Exception:
            logging.exception("write ocr raw debug failed")

        # -------- 选择优先结果 --------
        result = raw_results["from_pil"] or raw_results["from_path"] or []

        # -------- 提取文本 --------
        text_list = []
        for line in result:
            for word_info in line:
                text = word_info[1][0]
                confidence = word_info[1][1] if len(word_info[1]) > 1 else None
                if text:
                    text_list.append({
                        "text": text,
                        "confidence": confidence
                    })

        return {"status": "success", "data": text_list}

    except Exception as e:
        logging.exception("parse_image failed")
        return {"status": "error", "message": str(e)}



def extract_text_and_info(image_path: str):
    """
    OCR 识别 + 信息抽取（兼容新旧 PaddleOCR 输出）
    提取：姓名、日期、医院、文档类型
    """
    try:
        ocr_instance = get_ocr()
        result = ocr_instance.ocr(image_path)

        text_lines = []

        if isinstance(result, list) and len(result) > 0:
            first = result[0]

            # ----- 新格式：包含 rec_texts -----
            if isinstance(first, dict) and 'rec_texts' in first:
                text_lines = first['rec_texts']

            # ----- 旧格式：列表嵌套 -----
            elif isinstance(first, list):
                for line in result:
                    for w in line:
                        try:
                            text_lines.append(w[1][0])
                        except:
                            continue

        # 过滤空文本
        text_lines = [t for t in text_lines if t]

        full_text = "\n".join(text_lines).strip()

    except Exception:
        logging.exception("extract_text_and_info failed")
        full_text = ""

    # -------- 正则抽取结构化信息 --------
    name_match = re.search(r"姓名[:：\s]*([\u4e00-\u9fa5·]{2,6})", full_text)
    date_match = re.search(r"(\d{4}[-/年]\d{1,2}[-/月]\d{1,2})", full_text)
    hospital_match = re.search(r"([\u4e00-\u9fa5A-Za-z0-9·\(\)（）\-]+(?:医院|门诊|中心))", full_text)

    # 文档类型识别规则
    doc_type = "门诊病历"
    if "检验" in full_text or "化验" in full_text:
        doc_type = "检验报告"
    elif "影像" in full_text or "检查" in full_text:
        doc_type = "检查报告"
    elif "病历" in full_text:
        doc_type = "病历"

    structured = {
        "name": name_match.group(1).strip() if name_match else "",
        "date": date_match.group(1) if date_match else "",
        "hospital": hospital_match.group(1).strip() if hospital_match else "",
        "type": doc_type
    }

    return full_text, structured
