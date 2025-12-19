# Omni-channel Analytics Pipeline: High-Throughput Data Processing Framework

[![Python Version](https://img.shields.io/badge/python-3.14-blue.svg)](https://www.python.org/downloads/release/python-314/)
[![Architecture](https://img.shields.io/badge/Architecture-Medallion-orange.svg)](#architecture)
[![Performance](https://img.shields.io/badge/Performance-Vectorized-green.svg)](#performance-optimization)

## 1. Executive Summary
Hệ thống được thiết kế theo mô hình **End-to-End Data Pipeline**, giải quyết bài toán xử lý dữ liệu quy mô lớn (Large-scale Data) trên tài nguyên phần cứng hạn chế. Framework này thực thi quy trình trích xuất, chuẩn hóa và phân tích từ nguồn dữ liệu đa dạng (Unstructured Logs, Semi-structured JSON, và Structured CSV) với tư duy **Memory-first** và **Computational Efficiency**.

Dự án áp dụng triết lý **Medallion Architecture**, chia tách luồng dữ liệu thành các lớp Layer biệt lập (Raw -> Silver -> Gold) để đảm bảo tính minh bạch và khả năng truy xuất nguồn gốc (Data Lineage).

---

## 2. Core Architecture & Design Patterns

### 🏗 Data Tiering (Medallion Model)
*   **Bronze (Raw Layer):** Lưu trữ dữ liệu gốc, chưa qua xử lý từ log hệ thống và giao dịch thô.
*   **Silver (Processed Layer):** Dữ liệu được cấu trúc hóa thông qua Regex Parsing, Schema Enforcement và Enrichment (Làm giàu dữ liệu).
*   **Gold (Analytics Layer):** Business-level aggregates, sẵn sàng cho hạ tầng BI và Reporting.

### 🛠 Engineering Pillars
*   **Streaming & Lazy Evaluation:** Sử dụng Python Generators và Iterator pattern để xử lý tập dữ liệu Terabyte-scale với bộ nhớ RAM không đổi (Constant Memory Footprint).
*   **Vectorized Operations:** Loại bỏ hoàn toàn vòng lặp Python truyền thống (R-Row level), thay thế bằng NumPy/Pandas Vectorization (C-Column level) nhằm tận dụng tối đa tập lệnh SIMD trên chip **Apple Silicon M2**.
*   **O(1) Complexity Mapping:** Tối ưu hóa logic Enrichment bằng cấu trúc Hash Map (Dictionary) để đạt hiệu suất tra cứu hằng số, triệt tiêu độ trễ khi quy mô metadata tăng trưởng.

---

## 3. Detailed Phase Breakdown

### Phase 1: High-Performance Log Ingestion (Regex-based Extraction)
*   **Mechanism:** Sử dụng **Pre-compiled Regular Expressions** với Named Capturing Groups để phân tách dữ liệu phi cấu trúc.
*   **Optimization:** Thực thi cơ chế **Streaming I/O**, đọc và parse dòng đơn (Line-by-line) giúp hệ thống miễn nhiễm với lỗi `Out-of-Memory (OOM)`.
*   **Validation:** Tích hợp logic lọc nhiễu và loại bỏ bản ghi không hợp lệ ngay tại tầng Ingestion để đảm bảo chất lượng dữ liệu hạ nguồn.

### Phase 2: Stateful Enrichment & Data Integrity
*   **Mechanism:** Ánh xạ dữ liệu Silver Layer với Product Metadata thông qua **ID-based Mapping**.
*   **Scalability:** Sử dụng **Set-based Deduplication** để xử lý bài toán khách hàng duy nhất (Unique Identity) với hiệu năng cao.
*   **Integrity:** Áp dụng cơ chế **Safe Lookup** (Dictionary `.get()`) để bảo vệ Pipeline khỏi các sự cố Schema không nhất quán hoặc thiếu hụt Metadata.

### Phase 3: Big Data Analytics & Batch Processing
*   **Mechanism:** Thực thi **Chunk-based Processing** (Khối lượng 500k-1M records/batch) cho tệp tin giao dịch khổng lồ.
*   **Computation:** Chuyển đổi trạng thái dữ liệu sang **NumPy Arrays** để thực hiện các phép toán tài chính (VAT, Revenue, Discount) với hiệu năng cấp độ thấp (Low-level performance).
*   **Aggregation:** Áp dụng **Two-step Aggregation** (Local-grouping then Global-merging) để tối ưu hóa việc nén dữ liệu trước khi xuất báo cáo.

---

## 4. Project Structure
```text
omnichannel_pipeline/
├── data/
│   ├── raw/             # Ingestion Landing Zone (Immutable)
│   ├── processed/       # Silver/Gold Layers (Curated Data)
│   └── metadata/        # Master Data & Configurations
├── src/                 # Enterprise-grade Source Code
│   ├── ingestion/       # Unstructured to Semi-structured logic
│   ├── transformation/  # Business logic & Enrichment
│   ├── analytics/       # Vectorized computation engine
│   └── utils/           # Shared Helpers & Global Configurations
├── scripts/             # Data Generators & Utility Tools
├── main.py              # Pipeline Orchestrator (Entry Point)
└── .gitignore           # Resource Protection Policy
```

---

## 5. Deployment & Execution

### Prerequisites
- Python 3.14 (Optimized for Apple Silicon ARM64)
- Virtual Environment (venv)

### Installation
```bash
# Clone the repository
git clone git@github.com:Sanglm2207/omnichannel_pipeline.git
cd omnichannel_pipeline

# Setup isolated environment
python3 -m venv venv
source venv/bin/activate

# Install high-performance dependencies
pip install -r requirements.txt
```

### Running the Pipeline
```bash
# 1. Initialize Large-scale Data Samples
python scripts/gen_ingestion_data.py
python scripts/gen_big_data.py

# 2. Execute End-to-End Pipeline
python main.py
```

---

## 6. Performance Benchmarks (Estimated on M2)
*   **Ingestion Speed:** ~500,000 lines/sec (Regex-heavy).
*   **Memory Usage:** < 200MB RAM (Stable during 100GB processing).
*   **Computation Efficiency:** NumPy Vectorization mang lại tốc độ vượt trội gấp **~100x** so với chuẩn Python lặp truyền thống.

---
*Designed for Scalability, Built for Performance.*