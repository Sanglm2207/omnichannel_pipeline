import re
import csv
import os
import logging

logger = logging.getLogger(__name__)

# Compile sẵn các pattern để dùng lại nhiều lần (tăng tốc độ)
# Pattern này tìm email hợp lệ, IP và trạng thái
LOG_PATTERN = re.compile(
    r"user:(?P<email>[\w\.-]+@[\w\.-]+\.\w+)\s+"  # Trích xuất email (Named Group)
    r"ip:(?P<ip>\d{1,3}(?:\.\d{1,3}){3})\s+"      # Trích xuất IP
    r"action:(?P<action>[\w:]+)\s*"               # Trích xuất hành động
    r"(?:status:(?P<status>[\w:]+))?"             # Trích xuất status (nếu có)
)

def run_ingestion():
    print(">>>>> Đang thực hiện Regex parse log...")
    raw_log_path = "data/raw/access.log"
    output_path = "data/processed/cleaned_logs.csv"
    
    # Đảm bảo thư mục processed tồn tại
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    cleaned_data = []

    # Dùng Context Manager và đọc từng dòng (Streaming)
    try:
        with open(raw_log_path, "r") as file:
            for line_num, line in enumerate(file, 1):
                match = LOG_PATTERN.search(line)
                
                if match:
                    # Trích xuất dữ liệu từ các Named Groups
                    entry = match.groupdict()
                    # Case Study: Chỉ lấy các bản ghi có liên quan đến 'purchase' hoặc 'login'
                    cleaned_data.append((
                        entry['email'], 
                        entry['ip'], 
                        entry['action'], 
                        entry['status'] or "N/A" # Xử lý dữ liệu thiếu
                    ))
                else:
                    logger.warning(f"Dòng {line_num} không đúng định dạng: {line.strip()}")

        # Ghi kết quả ra CSV sạch
        headers = ["email", "ip", "action", "status"]
        with open(output_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(cleaned_data)
            
        logger.info(f"Đã xử lý xong {len(cleaned_data)} dòng log. Lưu tại {output_path}")

    except FileNotFoundError:
        logger.error(f"Không tìm thấy file log tại {raw_log_path}")
    except Exception as e:
        logger.error(f"Lỗi không xác định: {e}")