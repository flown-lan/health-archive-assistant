import sys
import json
from PIL import Image
from backend.app.ocr import parser
import os

img = sys.argv[1] if len(sys.argv) > 1 else "/Users/lanzf/Downloads/FT.png"
out = {"from_pil": None, "from_path": None, "errors": []}

ocr = None
try:
    ocr = parser.get_ocr()
except Exception as e:
    out["errors"].append(f"get_ocr error: {e}")

# try from PIL image
try:
    im = Image.open(img).convert("RGB")
    out["from_pil"] = ocr.ocr(im) if ocr else None
except Exception as e:
    out["errors"].append(f"ocr from PIL error: {e}")

# try from path
try:
    out["from_path"] = ocr.ocr(img) if ocr else None
except Exception as e:
    out["errors"].append(f"ocr from path error: {e}")

# write debug json
dbg = os.path.join(os.getcwd(), "backend", "ocr_raw_debug.json")
with open(dbg, "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=2)

print(json.dumps(out, ensure_ascii=False, indent=2))
print("wrote debug file:", dbg)