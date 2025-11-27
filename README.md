# 🇨🇳 中文版 README（专业版）

# 📁 PaperHealth – 个人健康档案助手（开源核心）

**PaperHealth** 是一个帮助用户将纸质病历、检验检查报告等医疗资料快速数字化、结构化并按时间管理的轻量级隐私友好型工具。

项目的初衷是解决现实中常见的问题：

* 医院信息不统一，纸质资料难以保存
* 不同医院的记录分散，难以整合
* 想回顾某次检查结果，却找不到对应文件
* 很多国家和地区缺乏完善的个人健康档案系统

为了让用户完全放心使用，**PaperHealth 核心功能将保持开源、本地运行，不上传任何隐私数据。**

---

## 🌟 项目定位（Open Core）

PaperHealth 采用 **「核心开源 + 可选增强功能」** 模式：

* **核心版本（开源）**：提供隐私安全、可验证的本地档案管理能力。
* **未来版本（可选增值）**：在 App Store 上可能加入高级功能（如云同步、家庭档案等），用于支持项目的持续开发。

核心开源版本将始终保持免费。

---

## 💡 核心功能（MVP）

1. **资料上传**：拍照 / 上传纸质病历与报告
2. **OCR 识别**：自动识别文本
3. **字段结构化**（MVP）

   * 文档类型
   * 医院名称
   * 就诊 / 检查日期
   * 患者姓名
4. **自动归档时间线**
5. **原图 + 识别文本查看**
6. **字段可手动编辑**

目标是：

> **让每张纸质病历自动变成可搜索、可追溯的健康档案。**

---

## 🚧 非 MVP（未来扩展）

这些功能不是 MVP 必要，但未来可能以免费或增值形式加入：

* AI 报告解读（非诊断）
* 家庭档案（多人管理）
* 多设备同步
* 健康指标趋势图
* PDF/JSON 导出
* 匿名分享（医生协助）
* 本地加密备份

---

## 🛠 技术栈（待定）

* **前端**：Next.js / React
* **后端**：FastAPI / Python
* **OCR**：可插拔（PaddleOCR / 自定义 LLM 模块）
* **数据库**：SQLite（MVP）
* **隐私**：默认全部本地处理

---

## 🤝 欢迎参与

欢迎你贡献以下内容：

* OCR 模型优化
* 信息抽取/分类增强
* UI 设计 & 前端开发
* 国际化语言支持
* 新的医疗文档类型

---

## 📜 许可证

（你可以选择 MIT / Apache 2.0 / AGPL —— 我可以根据需求帮你挑选最佳的一种）

---

---

# 🇺🇸 English README (Professional Version)

# 📁 PaperHealth – Personal Health Record Assistant (Open Core)

**PaperHealth** is a lightweight, privacy-friendly tool that helps users digitize, structure, and organize their paper medical documents — such as visit notes, lab reports, and imaging results — into searchable personal health records.

The project is designed to solve real-world problems:

* Medical documents are often paper-based and easy to lose
* Records from different hospitals are scattered and unstructured
* It’s hard to recall *when* a test was done and *what the result was*
* Many regions lack a robust personal health record system

To ensure user privacy and transparency, **the core features of PaperHealth will remain open-source and run entirely on-device.**

---

## 🌟 Project Model (Open Core)

PaperHealth follows an **“Open Core + Optional Premium Features”** model:

* **Core Version (Open Source)**

  * Fully local processing
  * No data uploaded
  * Free and privacy-safe

* **Future Versions (Optional Paid Add-ons)**

  * Premium features may be offered through App Store builds
  * Helps sustain long-term development

The **core open-source version will always remain free.**

---

## 💡 Core MVP Features

1. **Upload medical documents** (photo or file)
2. **OCR text recognition**
3. **Basic structured data extraction**

   * Document type
   * Hospital name
   * Date of visit/test
   * Patient name
4. **Automatic timeline organization**
5. **View original image + recognized text**
6. **Editable fields**

Goal:

> **Turn every paper medical document into a clean, searchable, structured health record.**

---

## 🚧 Non-MVP (Future Enhancements)

These may be added later as free or premium features:

* AI report summaries (non-diagnostic)
* Multi-person family profiles
* Cloud sync / multi-device access
* Health trend charts
* PDF / JSON export
* Anonymous share links
* Secure local encrypted backup

---

## 🛠 Tech Stack (Tentative)

* **Frontend:** Next.js / React
* **Backend:** FastAPI (Python)
* **OCR:** Pluggable (PaddleOCR / LLM-based extraction)
* **Database:** SQLite for MVP
* **Privacy:** All local by default

---

## 🤝 Contributing

Contributions are welcome:

* OCR improvements
* Better document classification
* Frontend design
* Localization
* New medical document types

---

## 📜 License

This project is licensed under the **Apache License 2.0**.
You are free to use, modify, distribute, and build upon this project, including for commercial purposes, as long as you comply with the terms of the license.

Please see the full license text in the LICENSE file.

本项目采用 **Apache 2.0 开源许可证** 发布。
你可以自由地使用、修改、分发本项目，包括商业用途，但必须遵循许可证条款。

完整的许可证内容请参见仓库中的 LICENSE 文件。