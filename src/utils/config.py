from pathlib import Path

# Định nghĩa thư mục gốc
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Định nghĩa các lớp dữ liệu (Data Tiers)
RAW_DIR = BASE_DIR / "data" / "raw"
SILVER_DIR = BASE_DIR / "data" / "processed"
METADATA_DIR = BASE_DIR / "data" / "metadata"

# Đường dẫn file cụ thể
LOG_FILE = RAW_DIR / "access.log"
TRANSACTION_FILE = RAW_DIR / "transactions_big.csv"
PRODUCT_METADATA = METADATA_DIR / "products.json"
CLEANED_LOG_CSV = SILVER_DIR / "cleaned_logs.csv"
ENRICHED_DATA_CSV = SILVER_DIR / "enriched_data.csv"
FINAL_REPORT_CSV = SILVER_DIR / "final_monthly_report.csv"

# Regex Pattern
LOG_REGEX = r"user:(?P<email>[\w\.-]+@[\w\.-]+\.\w+)\s+ip:(?P<ip>\d{1,3}(?:\.\d{1,3}){3})\s+action:(?P<action>[\w:]+)\s*(?:status:(?P<status>[\w:]+))?"