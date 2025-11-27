# PaperHealth API 设计 (API Design)

## 基础 URL
所有 API 以 `/api` 开头，例如：`/api/upload`

## 1. 上传图片
- **URL**: `/api/upload`
- **方法**: POST
- **参数**: 单文件或多文件 `file`
- **返回示例**:
```json
{
  "record_id": 1,
  "image_path": "local/path/to/image.jpg",
  "raw_text": "OCR 提取内容",
  "structured": {
    "name": "张三",
    "date": "2025-11-27",
    "hospital": "某医院",
    "type": "检验报告"
  }
}
```

## 2. 获取时间线
- **URL**: `/api/records`
- **方法**: GET
- **返回示例**:
```json
[
  {
    "record_id": 1,
    "name": "张三",
    "date": "2025-11-27",
    "hospital": "某医院",
    "type": "检验报告"
  }
]
```

## 3. 查看单条记录详情
- **URL**: `/api/records/{id}`
- **方法**: GET
- **返回示例**:
```json
{
  "record_id": 1,
  "image_path": "local/path/to/image.jpg",
  "raw_text": "OCR 提取内容",
  "structured": {
    "name": "张三",
    "date": "2025-11-27",
    "hospital": "某医院",
    "type": "检验报告"
  }
}
```

## 4. 编辑记录
- **URL**: `/api/records/{id}`
- **方法**: PUT
- **参数**: JSON
```json
{
  "structured": {
    "name": "张三",
    "date": "2025-11-27",
    "hospital": "某医院",
    "type": "门诊病历"
  }
}
```
- **返回**: 更新后的记录
