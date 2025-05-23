from data_collector import StockDataCollector
import pandas as pd

def main():
    # 데이터 수집기 초기화
    collector = StockDataCollector()
    
    # 테스트할 주식 심볼들
    symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'PLTR']
    
    # 각 심볼에 대해 데이터 수집
    for symbol in symbols:
        print(f"\nFetching data for {symbol}...")
        df = collector.fetch_stock_data(symbol)
        
        if not df.empty:
            print(f"Successfully fetched {len(df)} records for {symbol}")
            print("\nFirst few records:")
            print(df.head())
            print("\nData columns:", df.columns.tolist())
            print("\nLast price:", df['Close'].iloc[-1])
            print("Daily change:", ((df['Close'].iloc[-1] - df['Close'].iloc[-2]) / df['Close'].iloc[-2] * 100).round(2), "%")
        else:
            print(f"Failed to fetch data for {symbol}")

if __name__ == "__main__":
    main() 