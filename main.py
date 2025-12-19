import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import logging
from ingestion.log_parser import run_ingestion
from transformation.enricher import run_transformation
from analytics.processor import run_analytics

# Cấu hình logging cơ bản để theo dõi pipeline
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    logger.info("--- KHỞI ĐỘNG OMNICHANNEL DATA PIPELINE ---")

    try:
        # Ingestion (Regex & File I/O)
        logger.info("PHASE 1: Bắt đầu xử lý Raw Logs...")
        run_ingestion()
        
        # Transformation (Dict/Set/Enrichment)
        logger.info("PHASE 2: Bắt đầu làm giàu dữ liệu (Data Enrichment)...")
        run_transformation()
        
        # Analytics (Pandas/NumPy)
        logger.info("PHASE 3: Bắt đầu tính toán Analytics...")
        run_analytics()

        logger.info("--- PIPELINE HOÀN THÀNH THÀNH CÔNG ---")

    except Exception as e:
        logger.error(f"!!! PIPELINE THẤT BẠI: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()