import json
import random
import os
import sys

# === ĐOẠN FIX ĐƯỜNG DẪN ===
# Lấy đường dẫn thư mục hiện tại (scripts/) -> lấy thư mục cha (gốc dự án)
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(root_path)
# ==========================

# Bây giờ import sẽ chạy mượt mà
from src.utils.config import LOG_FILE, PRODUCT_METADATA

def gen_metadata(path):
    """Tạo file metadata sản phẩm mẫu"""
    products = {
        f"p_{str(i).zfill(3)}": {
            "name": f"Sản phẩm {i}",
            "price": random.randint(10, 2000),
            "category": random.choice(["Tech", "Fashion", "Home", "Books"])
        } for i in range(1, 101)
    }
    
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(products, f, indent=4, ensure_ascii=False)
    print(f"✅ Đã tạo Metadata tại: {path}")
    return list(products.keys())

def gen_raw_logs(path, product_ids, num_lines=1000000):
    """Tạo file log thô với hàng triệu dòng"""
    emails = ["hoang@work.com", "lan@service.vn", "minh@company.com", "guest@test.io"]
    actions = ["login", "logout", "view_product", "click_ads"]
    statuses = ["success", "failed", "pending", "404"]
    
    os.makedirs(os.path.dirname(path), exist_ok=True)
    print(f"🚀 Đang tạo {num_lines:,} dòng log tại: {path}...")
    
    with open(path, 'w') as f:
        for i in range(num_lines):
            email = random.choice(emails)
            ip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
            action = random.choice(actions)
            status = random.choice(statuses)
            timestamp = "2025-12-19 17:00:00"
            
            if action == "view_product":
                p_id = random.choice(product_ids)
                action_str = f"{action}:{p_id}"
            else:
                action_str = action

            # Dòng lỗi (test Regex)
            if i % 1000 == 0:
                f.write(f"{timestamp} ERROR user:bad-email-format ip:0.0.0.0 action:unknown\n")
            else:
                line = f"{timestamp} INFO user:{email} ip:{ip} action:{action_str} status:{status}\n"
                f.write(line)
                
    print(f"✅ Hoàn thành tạo Log!")

if __name__ == "__main__":
    # 1. Tạo Metadata trước để lấy danh sách ID
    p_ids = gen_metadata(str(PRODUCT_METADATA))
    
    # 2. Tạo Log dựa trên danh sách ID đó
    gen_raw_logs(str(LOG_FILE), p_ids, num_lines=1000000)