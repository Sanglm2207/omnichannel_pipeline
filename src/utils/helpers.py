import json
import csv
import re
import logging
from typing import Generator, Dict, List, Union

logger = logging.getLogger(__name__)

def load_json(path: str) -> Dict:
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading JSON at {path}: {e}")
        return {}

def parse_file_with_regex(file_path: str, regex_pattern: str) -> Generator[Dict, None, None]:
    """Hàm tổng quát: Đọc file và parse theo Regex, trả về Generator"""
    pattern = re.compile(regex_pattern)
    try:
        with open(file_path, "r") as f:
            for line in f:
                match = pattern.search(line)
                if match:
                    yield match.groupdict()
    except FileNotFoundError:
        logger.error(f"File không tồn tại: {file_path}")

def save_to_csv(data_iterator: Union[Generator, List], path: str, headers: List[str]):
    """Hàm tổng quát: Ghi dữ liệu từ List hoặc Generator vào CSV"""
    try:
        with open(path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            # Ghi từng dòng để tối ưu bộ nhớ
            for row in data_iterator:
                # Chỉ ghi những trường có trong headers (tránh lỗi dư thừa field)
                filtered_row = {k: row.get(k, "N/A") for k in headers}
                writer.writerow(filtered_row)
        logger.info(f"Đã lưu dữ liệu vào CSV thành công: {path}")
    except Exception as e:
        logger.error(f"Lỗi ghi CSV tại {path}: {e}")