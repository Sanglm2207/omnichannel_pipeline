import pandas as pd
import numpy as np
import os
import json
import logging

logger = logging.getLogger(__name__)

def run_analytics():
    transaction_path = "data/raw/transactions_big.csv"
    metadata_path = "data/metadata/products.json"
    output_path = "data/processed/final_monthly_report.csv"

    if not os.path.exists(transaction_path):
        logger.error("Chưa có file transactions_big.csv. Hãy chạy script gen_big_data.py trước!")
        return

    # 1. LOAD METADATA (Dùng để mapping giá trong lúc xử lý chunk)
    with open(metadata_path, 'r') as f:
        products = json.load(f)
    
    # Tạo một Series để lookup giá nhanh hơn trong Pandas
    price_map = {k: v['price'] for k, v in products.items()}
    cat_map = {k: v['category'] for k, v in products.items()}

    # 2. XỬ LÝ CHUNK (Kỹ thuật sống còn cho Big Data)
    # Chúng ta đọc mỗi lần 500,000 dòng để không làm treo máy
    chunk_size = 500000
    aggregated_results = []

    logger.info("Bắt đầu xử lý file lớn bằng kỹ thuật Chunking...")

    # Dùng pandas read_csv với iterator=True
    reader = pd.read_csv(transaction_path, chunksize=chunk_size)

    for i, chunk in enumerate(reader):
        # A. Mapping thông tin từ Metadata
        chunk['unit_price'] = chunk['product_id'].map(price_map)
        chunk['category'] = chunk['product_id'].map(cat_map)
        
        # B. Xử lý Datetime: Chuyển đổi và trích xuất tháng
        chunk['date'] = pd.to_datetime(chunk['date'])
        chunk['month'] = chunk['date'].dt.to_period('M')

        # C. TỐI ƯU NUMPY: Tính toán Vectorized (Nhanh gấp 100 lần vòng lặp)
        # Tính doanh thu chưa thuế
        qty_array = chunk['qty'].values
        price_array = chunk['unit_price'].values
        
        chunk['raw_revenue'] = qty_array * price_array
        
        # Tính VAT 10% bằng NumPy
        chunk['vat'] = chunk['raw_revenue'].values * 0.1
        
        # Doanh thu cuối cùng
        chunk['total_revenue'] = chunk['raw_revenue'] + chunk['vat']

        # D. AGGREGATION CỤC BỘ: Groupby ngay trong chunk để giảm dung lượng dữ liệu
        summary = chunk.groupby(['month', 'category']).agg({
            'total_revenue': 'sum',
            'order_id': 'count'
        }).reset_index()
        
        aggregated_results.append(summary)
        
        if (i + 1) % 10 == 0:
            logger.info(f"Đã xử lý: {(i + 1) * chunk_size:,} dòng...")

    # 3. TỔNG HỢP CUỐI CÙNG (Merge các kết quả từ các chunk)
    final_df = pd.concat(aggregated_results)
    final_report = final_df.groupby(['month', 'category']).sum().reset_index()

    # Lưu kết quả
    final_report.to_csv(output_path, index=False)
    logger.info(f"Báo cáo cuối cùng đã được xuất tại: {output_path}")
    print("\n--- KẾT QUẢ PHÂN TÍCH ---")
    print(final_report.head(10))