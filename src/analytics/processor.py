import pandas as pd
import numpy as np
from src.utils.config import TRANSACTION_FILE, PRODUCT_METADATA, FINAL_REPORT_CSV
from src.utils.helpers import load_json

def calculate_metrics(df: pd.DataFrame, price_map: dict) -> pd.DataFrame:
    """Hàm thuần túy chỉ tính toán số liệu"""
    df['unit_price'] = df['product_id'].map(price_map)
    
    # Vectorized calculation
    raw_rev = df['qty'].values * df['unit_price'].values
    df['total_revenue'] = raw_rev * 1.1 # Bao gồm 10% VAT
    
    df['month'] = pd.to_datetime(df['date']).dt.to_period('M')
    return df.groupby(['month', 'product_id'])['total_revenue'].sum().reset_index()


def run_analytics():
    products = load_json(PRODUCT_METADATA)
    price_map = {k: v['price'] for k, v in products.items()}
    
    # Xử lý theo chunk nhưng dùng hàm calculate_metrics đã tách riêng
    chunks = pd.read_csv(TRANSACTION_FILE, chunksize=500000)
    summaries = [calculate_metrics(chunk, price_map) for chunk in chunks]
    
    final_df = pd.concat(summaries).groupby(['month', 'product_id']).sum().reset_index()
    final_df.to_csv(FINAL_REPORT_CSV, index=False)