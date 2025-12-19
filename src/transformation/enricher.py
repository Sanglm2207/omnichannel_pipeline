import json
import csv
import os
import logging

logger = logging.getLogger(__name__)

def load_product_metadata(path):
    """Sử dụng Dictionary để tối ưu tra cứu O(1)"""
    try:
        with open(path, 'r') as f:
            # Case Study: JSON Parsing
            return json.load(f)
    except Exception as e:
        logger.error(f"Lỗi đọc Metadata: {e}")
        return {}

def run_transformation():
    log_data_path = "data/processed/cleaned_logs.csv"
    metadata_path = "data/metadata/products.json"
    output_path = "data/processed/enriched_data.csv"

    # 1. Load Metadata vào Dictionary (Key là Product_ID)
    # Metadata có dạng: {"p_001": {"name": "iPhone", "price": 1000, "category": "Tech"}}
    products = load_product_metadata(metadata_path)

    enriched_results = []
    
    # 2. Sử dụng SET để quản lý danh sách khách hàng VIP (không trùng lặp)
    # Giả sử chúng ta muốn theo dõi các khách hàng có hành động 'view_product'
    potential_customers = set()

    if not os.path.exists(log_data_path):
        logger.error("Không tìm thấy dữ liệu từ Phase 1!")
        return

    # 3. Đọc dữ liệu đã cleaned và thực hiện Mapping
    with open(log_data_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            email = row['email']
            action = row['action']
            
            # Giả sử trong Log action có dạng 'view_product:p_001'
            if 'view_product' in action:
                # Tách ID sản phẩm từ chuỗi action
                p_id = action.split(':')[-1] if ':' in action else None
                
                # CASE STUDY: Dictionary Lookup O(1)
                # Thay vì lặp qua danh sách sản phẩm, ta truy cập thẳng bằng Key
                product_info = products.get(p_id)
                
                if product_info:
                    enriched_results.append({
                        "email": email,
                        "product_id": p_id,
                        "product_name": product_info['name'],
                        "category": product_info['category'],
                        "price": product_info['price']
                    })
                    potential_customers.add(email) # Tự động loại bỏ trùng lặp

    # 4. Ghi dữ liệu đã làm giàu ra file Silver layer
    if enriched_results:
        headers = enriched_results[0].keys()
        with open(output_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(enriched_results)
            
        logger.info(f"Enrichment hoàn tất: {len(enriched_results)} bản ghi.")
        logger.info(f"Tìm thấy {len(potential_customers)} khách hàng tiềm năng độc nhất.")
    else:
        logger.warning("Không có dữ liệu để làm giàu.")