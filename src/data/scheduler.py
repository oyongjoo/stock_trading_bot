import schedule
import time
from datetime import datetime
from data_collector import StockDataCollector
import logging

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data_collection.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def collect_daily_data():
    """매일 주식 데이터를 수집하는 함수"""
    try:
        collector = StockDataCollector()
        symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'PLTR']
        
        for symbol in symbols:
            logger.info(f"Collecting data for {symbol}")
            df = collector.fetch_stock_data(symbol)
            
            if not df.empty:
                logger.info(f"Successfully collected {len(df)} records for {symbol}")
                logger.info(f"Latest price: {df['Close'].iloc[-1]}")
            else:
                logger.warning(f"Failed to collect data for {symbol}")
                
    except Exception as e:
        logger.error(f"Error in daily data collection: {str(e)}")

def main():
    """스케줄러 메인 함수"""
    logger.info("Starting data collection scheduler")
    
    # 매일 장 마감 후 1시간 후에 데이터 수집 (미국 동부시간 기준 17:00)
    schedule.every().day.at("18:00").do(collect_daily_data)
    
    # 프로그램 시작시 즉시 한번 실행
    collect_daily_data()
    
    # 스케줄러 실행
    while True:
        schedule.run_pending()
        time.sleep(60)  # 1분마다 스케줄 체크

if __name__ == "__main__":
    main() 