# Omni-channel Analytics Pipeline v1.0

## 1. Giới thiệu (Overview)
Dự án này mô phỏng một hệ thống xử lý dữ liệu (Data Pipeline) thực tế cho một doanh nghiệp bán lẻ đa kênh. Hệ thống thu thập dữ liệu từ các nguồn khác nhau (Logs, JSON Metadata, CSV Transactions) để làm sạch, chuẩn hóa và trích xuất các chỉ số kinh doanh quan trọng.

**Mục tiêu kỹ thuật:** Triển khai các kỹ thuật tối ưu hóa Python 3.14 cho xử lý dữ liệu lớn, tập trung vào bộ nhớ, tốc độ thực thi và tính ổn định của mã nguồn.

---

## 2. Kiến trúc dữ liệu (Data Architecture)
Dữ liệu di chuyển qua các giai đoạn theo mô hình **Medallion Architecture** (đơn giản hóa):
1.  **Bronze (Raw):** Dữ liệu thô từ log hệ thống, file JSON cấu hình và file giao dịch CSV.
2.  **Silver (Cleaned):** Dữ liệu đã được parse bằng Regex, xử lý các lỗi định dạng và lọc bỏ email/IP rác.
3.  **Gold (Aggregated):** Kết quả cuối cùng được tính toán bằng Pandas/NumPy, sẵn sàng cho Business Intelligence (BI).

---

## 3. Cấu trúc thư mục (Project Structure)
```text
omnichannel_pipeline/
├── data/
│   ├── raw/           # Dữ liệu gốc (access.log, transactions.csv)
│   ├── metadata/      # Dữ liệu cấu hình, danh mục (products.json)
│   └── processed/     # Kết quả sau khi xử lý (final_report.csv)
├── scripts/           # Logic xử lý chính
│   ├── ingestion.py   # Xử lý Log & Regex (Phase 1)
│   ├── enrichment.py  # Xử lý Cấu trúc dữ liệu & Mapping (Phase 2)
│   └── analytics.py   # Xử lý Pandas & NumPy (Phase 3)
├── logs/              # Nhật ký vận hành hệ thống
├── notebooks/         # Thử nghiệm logic nhanh
├── venv/              # Môi trường ảo Python 3.14
└── README.md          # Tài liệu dự án
```

---

## 4. Các tình huống nghiên cứu (Case Studies)

### 🧩 Case Study 1: High-Performance Log Ingestion (Regex & File I/O)
*   **Vấn đề:** File log hệ thống có thể nặng hàng GB, chứa nhiều thông tin nhiễu.
*   **Giải pháp DE:**
    *   Sử dụng **Context Manager (`with open`)** để stream dữ liệu từng dòng, tránh nạp toàn bộ vào RAM.
    *   Áp dụng **Regular Expression (Regex)** để trích xuất email khách hàng hợp lệ và lọc các hành động lỗi.
    *   Tối ưu hóa tốc độ bằng cách `compile` các Regex pattern trước khi lặp.

### 🔗 Case Study 2: Intelligent Data Enrichment (Data Structures)
*   **Vấn đề:** Cần ánh xạ thông tin sản phẩm từ file JSON vào các giao dịch với tốc độ cao nhất.
*   **Giải pháp DE:**
    *   Sử dụng **Dictionary** để lưu trữ Metadata sản phẩm, biến việc tra cứu từ $O(n)$ thành $O(1)$.
    *   Sử dụng **Set** để lọc danh sách khách hàng duy nhất (Deduplication) và so sánh giữa các tập dữ liệu.
    *   Sử dụng **Tuple** để lưu trữ các bản ghi sau khi dọn dẹp để đảm bảo tính bất biến (Data Integrity).

### 📈 Case Study 3: Vectorized Business Analytics (Pandas & NumPy)
*   **Vấn đề:** Tính toán thuế VAT, chiết khấu và doanh thu theo tháng cho hàng triệu dòng giao dịch.
*   **Giải pháp DE:**
    *   Dùng **Pandas DataFrame** để thực hiện các phép Join/Merge dữ liệu đa nguồn.
    *   Dùng **NumPy Vectorization** thay cho vòng lặp `for` để thực hiện các phép tính số học trên cột, tận dụng sức mạnh của chip M2.
    *   Xử lý chuỗi thời gian bằng **Pandas Datetime** để phân tích xu hướng theo ngày/tháng/năm.

---

## 5. Hướng dẫn cài đặt & Chạy (Usage)

### Yêu cầu hệ thống:
*   Python 3.14+
*   MacBook M1/M2/M3 (Khuyên dùng để tối ưu ARM)

### Thiết lập môi trường:
1. Kích hoạt môi trường ảo:
   ```bash
   source venv/bin/activate
   ```
2. Cài đặt thư viện:
   ```bash
   pip install pandas numpy
   ```

### Thực thi Pipeline:
*   **B1:** Chạy Ingestion để dọn dẹp logs.
*   **B2:** Chạy Enrichment để chuẩn hóa dữ liệu.
*   **B3:** Chạy Analytics để xuất báo cáo cuối cùng.

---

## 6. Ghi chú về Tối ưu hóa (Performance Notes)
*   Dự án ưu tiên sử dụng **Generator** thay vì **List** khi xử lý file lớn.
*   Hạn chế tối đa việc sử dụng hàm `.apply()` trong Pandas, thay thế bằng các hàm native của NumPy để đạt hiệu năng tốt nhất trên chip Apple Silicon.

---

**Xác nhận:** Bạn đã lưu file này chưa? Sau đó chúng ta sẽ đi vào viết logic "không code" nhưng cực kỳ chi tiết cho **Phase 1: Ingestion & Regex** dựa trên đúng cấu trúc này.