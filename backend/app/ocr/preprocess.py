import cv2
import numpy as np
from PIL import Image
import io

def load_image(image_bytes: bytes):
    """将 bytes 转为 OpenCV 图像（BGR）"""
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

def resize_image(img, max_side=1280):
    """
    限制最长边 <= max_side（OCR官方推荐：960~1280）
    大幅提升 OCR 速度
    """
    h, w = img.shape[:2]
    scale = max_side / max(h, w)
    if scale >= 1:
        return img  # 不缩放
    new_w, new_h = int(w * scale), int(h * scale)
    return cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)

def to_gray(img):
    """灰度化"""
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def adaptive_threshold(img):
    """
    自适应阈值（对医院浅色背景特别有效）
    让文字更清晰
    """
    return cv2.adaptiveThreshold(
        img,
        255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY,
        35,
        10
    )

def denoise(img):
    """轻度去噪（保持文字锐度）"""
    return cv2.fastNlMeansDenoising(img, h=15)

def enhance_contrast(img):
    """直方图均衡，提升字符对比度"""
    return cv2.equalizeHist(img)

def preprocess_image_bytes(image_bytes: bytes) -> bytes:
    """
    输入：原始图片 bytes
    输出：预处理后的图片 bytes（可直接送给 OCR）
    """
    img = load_image(image_bytes)

    # 步骤 1：缩放（最重要）
    img = resize_image(img, max_side=1280)

    # 步骤 2：灰度化
    img = to_gray(img)

    # 步骤 3：增强对比度
    img = enhance_contrast(img)

    # 步骤 4：自适应阈值（关键）
    img = adaptive_threshold(img)

    # 步骤 5：轻去噪
    img = denoise(img)

    # 转回 bytes（PNG 防止失真）
    _, buffer = cv2.imencode(".png", img)
    return buffer.tobytes()

def preprocess_image(image_input):
    if isinstance(image_input, str):
        img = cv2.imread(image_input)
    elif isinstance(image_input, Image.Image):
        img = cv2.cvtColor(np.array(image_input), cv2.COLOR_RGB2BGR)
    else:
        raise TypeError("image_input 必须是文件路径或PIL.Image")
    
    # 关键优化：针对高分辨率图片（>2MP）强制缩小到 640px
    h, w = img.shape[:2]
    pixels = h * w / 1e6  # 百万像素
    
    if pixels > 2:  # 超过 200万像素
        max_side = 640  # 强制缩小（速度提升 3-5 倍）
    else:
        max_side = 960  # 正常尺寸
    
    img = resize_image(img, max_side=max_side)
    
    # 简化预处理（只做对比度增强）
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    enhanced = clahe.apply(gray)
    result = cv2.cvtColor(enhanced, cv2.COLOR_GRAY2RGB)
    return result
