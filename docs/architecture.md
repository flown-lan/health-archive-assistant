# PaperHealth 架构说明 (Architecture)

## 1. 项目总体架构
PaperHealth 是一个 **本地优先 (local-first)、开源的健康档案管理系统**，主要功能是将纸质病历拍照后整理为电子健康档案。
主要模块：
```
用户 → 前端 (React/TypeScript) → 后端 (FastAPI/Python) → 本地存储/数据库
```

## 2. 模块说明
### 前端 (frontend)
- 上传图片
- 展示时间线
- 展示单条记录详情
- 本地状态管理，界面友好

### 后端 (backend)
- FastAPI 提供 REST API
- 图片接收和存储
- OCR 文字识别
- 结构化信息抽取
- SQLite 数据库存储

### 数据存储
- 图片文件存储在本地文件夹
- 数据结构：
  - id
  - patient_name
  - document_type
  - hospital
  - date
  - raw_text
  - structured_json
  - image_path

## 3. 数据流
1. 用户在前端上传图片  
2. 后端接收图片 → 保存本地  
3. OCR 模块识别图片文字 → 返回原始文本  
4. 信息抽取模块生成结构化数据  
5. 数据存入 SQLite  
6. 前端时间线 API 获取结构化数据展示  
7. 用户可点击记录查看详情或编辑字段
