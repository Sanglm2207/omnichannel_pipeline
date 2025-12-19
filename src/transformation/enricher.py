import csv
import logging
from typing import Generator, Dict
from src.utils.config import CLEANED_LOG_CSV, PRODUCT_METADATA, ENRICHED_DATA_CSV
from src.utils.helpers import load_json, save_to_csv

logger = logging.getLogger(__name__)

def enrich_data_stream(log_path: str, metadata: Dict) -> Generator[Dict, None, None]:
    """
    Generator function: Đọc từng dòng log đã clean, map với metadata và yield kết quả.
    Tối ưu: RAM không đổi bất kể file log lớn bao nhiêu.
    """
    try:
        with open(log_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                action = row.get('action', '')
                
                # Logic: Chỉ xử lý các hành động có chứa ID sản phẩm (ví dụ: view_product:p_001)
                if 'view_product' in action:
                    p_id = action.split(':')[-1] if ':' in action else None
                    product_info = metadata.get(p_id)
                    
                    if product_info:
                        # Trả về một dictionary đã được "làm giàu" thông tin
                        yield {
                            "email": row['email'],
                            "product_id": p_id,
                            "product_name": product_info['name'],
                            "category": product_info['category'],
                            "price": product_info['price']
                        }
    except FileNotFoundError:
        logger.error(f"Không tìm thấy file: {log_path}")

def run_transformation():
    logger.info("Bắt đầu Phase 2: Enrichment (Streaming Mode)...")

    # 1. Load Metadata (Dictionary - Lookup O(1))
    products = load_json(str(PRODUCT_METADATA))
    if not products:
        logger.error("Metadata rỗng, dừng transformation.")
        return

    # 2. Khởi tạo generator để xử lý dữ liệu
    enriched_gen = enrich_data_stream(str(CLEANED_LOG_CSV), products)

    # 3. Định nghĩa các cột đầu ra
    headers = ["email", "product_id", "product_name", "category", "price"]

    # 4. Sử dụng Helper save_to_csv để ghi dữ liệu theo kiểu streaming
    save_to_csv(
        data_iterator=enriched_gen,
        path=str(ENRICHED_DATA_CSV),
        headers=headers
    )