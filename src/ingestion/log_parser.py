import logging
from src.utils.config import LOG_FILE, CLEANED_LOG_CSV, LOG_REGEX
from src.utils.helpers import parse_file_with_regex, save_to_csv

logger = logging.getLogger(__name__)

def run_ingestion():
    logger.info("Bắt đầu Ingestion sử dụng Helper Tools...")
    
    # Khởi tạo generator (chưa tốn RAM)
    log_generator = parse_file_with_regex(LOG_FILE, LOG_REGEX)
    
    # Định nghĩa các cột muốn giữ lại
    headers = ["email", "ip", "action", "status"]
    
    # Sử dụng helper để ghi file
    save_to_csv(
        data_iterator=log_generator, 
        path=str(CLEANED_LOG_CSV), 
        headers=headers
    )