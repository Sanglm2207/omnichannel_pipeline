import csv
import random
import os
import time
from datetime import datetime, timedelta

def generate_big_data(file_path, target_size_gb=1):
    # 1. CẤU HÌNH DỮ LIỆU MẪU (Để mapping khớp với products.json)
    emails = [f"user_{i}@gmail.com" for i in range(1, 1001)]
    product_ids = [f"p_00{i}" for i in range(1, 4)] # p_001, p_002, p_003
    start_date = datetime(2025, 1, 1)

    # Tính toán kích thước
    target_bytes = target_size_gb * 1024 * 1024 * 1024
    current_bytes = 0
    row_count = 0
    
    # 2. KHỞI TẠO FILE
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    print(f"🚀 Đang khởi tạo file {target_size_gb}GB tại: {file_path}")
    start_time = time.time()

    with open(file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        # Viết Header
        writer.writerow(["order_id", "customer_email", "product_id", "qty", "date"])
        
        # 3. GHI THEO BATCH (Để tối ưu tốc độ ghi đĩa)
        batch_size = 100000 
        while current_bytes < target_bytes:
            batch_data = []
            for _ in range(batch_size):
                row_count += 1
                # Tạo dòng dữ liệu ngẫu nhiên
                order_id = row_count
                email = random.choice(emails)
                p_id = random.choice(product_ids)
                qty = random.randint(1, 5)
                # Random ngày trong năm 2025
                dt = start_date + timedelta(days=random.randint(0, 364), seconds=random.randint(0, 86400))
                date_str = dt.strftime("%Y-%m-%d %H:%M:%S")
                
                batch_data.append([order_id, email, p_id, qty, date_str])
            
            writer.writerows(batch_data)
            
            # Cập nhật dung lượng hiện tại
            current_bytes = f.tell()
            progress = (current_bytes / target_bytes) * 100
            elapsed = time.time() - start_time
            print(f"⏳ Đã ghi: {current_bytes/(1024**3):.2f} GB ({progress:.1f}%) - Time: {elapsed:.1f}s", end='\r')

    print(f"\n✅ Hoàn thành!")
    print(f"📊 Tổng số dòng: {row_count:,}")
    print(f"⏱️ Thời gian thực hiện: {time.time() - start_time:.1f} giây")

if __name__ == "__main__":
    # Với mục đích học tập, 1GB (~15 triệu dòng) là đủ để thấy sức mạnh của Chunking
    path = "data/raw/transactions_big.csv"
    generate_big_data(path, target_size_gb=1)