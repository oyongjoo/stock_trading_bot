import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.data.data_collector import StockDataCollector
from src.strategy.technical_indicators import TechnicalIndicators
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import logging

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def plot_indicators(symbol: str, data: pd.DataFrame, indicators: TechnicalIndicators):
    """기술적 지표 시각화"""
    try:
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(15, 12), gridspec_kw={'height_ratios': [3, 1, 1]})
        
        # 가격 차트와 이동평균선
        ax1.plot(data.index, data['Close'], label='Close', color='black')
        ax1.plot(data.index, data['SMA_20'], label='SMA 20', color='blue')
        ax1.plot(data.index, data['SMA_60'], label='SMA 60', color='red')
        ax1.plot(data.index, data['BB_upper'], label='BB Upper', color='gray', linestyle='--')
        ax1.plot(data.index, data['BB_lower'], label='BB Lower', color='gray', linestyle='--')
        ax1.set_title(f'{symbol} Price and Moving Averages')
        ax1.legend()
        ax1.grid(True)
        
        # RSI
        ax2.plot(data.index, data['RSI'], label='RSI', color='purple')
        ax2.axhline(y=70, color='r', linestyle='--')
        ax2.axhline(y=30, color='g', linestyle='--')
        ax2.set_title('RSI')
        ax2.legend()
        ax2.grid(True)
        
        # MACD
        ax3.plot(data.index, data['MACD'], label='MACD', color='blue')
        ax3.plot(data.index, data['MACD_signal'], label='Signal', color='red')
        ax3.bar(data.index, data['MACD_hist'], label='Histogram', color='gray', alpha=0.3)
        ax3.set_title('MACD')
        ax3.legend()
        ax3.grid(True)
        
        plt.tight_layout()
        
        # 저장 경로 생성
        save_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'backtest_results')
        os.makedirs(save_dir, exist_ok=True)
        
        # 파일 저장
        save_path = os.path.join(save_dir, f'{symbol}_indicators_{datetime.now().strftime("%Y%m%d")}.png')
        plt.savefig(save_path)
        plt.close()
        logger.info(f"Chart saved to {save_path}")
        
    except Exception as e:
        logger.error(f"Error plotting indicators for {symbol}: {str(e)}")
        plt.close()

def main():
    # 데이터 수집
    collector = StockDataCollector()
    
    # 분석 대상 종목
    symbols = {
        # AI/반도체 관련
        'NVDA': 'NVIDIA (AI 반도체)',  # AI 반도체 선두주
        'AMD': 'AMD (반도체)',         # AI 반도체 경쟁사
        'INTC': 'Intel (반도체)',      # 반도체 제조
        'AVGO': 'Broadcom (반도체)',   # AI 네트워킹 칩
        'MU': 'Micron (메모리)',       # AI 메모리
        
        # AI 소프트웨어/서비스
        'MSFT': 'Microsoft (AI)',      # AI 클라우드/소프트웨어
        'GOOGL': 'Google (AI)',        # AI 검색/클라우드
        'META': 'Meta (AI)',           # AI 소셜미디어
        'CRM': 'Salesforce (AI)',      # AI 기업용 소프트웨어
        'PLTR': 'Palantir (AI)',       # AI 데이터 분석
        
        # 전기차/배터리
        'TSLA': 'Tesla (전기차)',      # 전기차 선두주
        'RIVN': 'Rivian (전기차)',     # 전기차 신흥주
        'LCID': 'Lucid (전기차)',      # 전기차 신흥주
        'QS': 'QuantumScape (배터리)', # 차세대 배터리
        'ENVX': 'Enovix (배터리)',     # 차세대 배터리
        
        # ESS/재생에너지
        'ENPH': 'Enphase (ESS)',       # 태양광 인버터
        'SEDG': 'SolarEdge (ESS)',     # 태양광 인버터
        'RUN': 'Sunrun (ESS)',         # 태양광 설치
        'STEM': 'Stem (ESS)',          # 에너지 저장
        'BE': 'Bloom Energy (ESS)',    # 수소 연료전지
        
        # AI/로봇 관련 ETF
        'BOTZ': 'Global Robotics & AI',  # 로봇/AI ETF
        'ARKQ': 'ARK Autonomous Tech',   # 자율주행/AI ETF
        'ROBO': 'Robo Global Robotics',  # 로봇공학 ETF
        'AIQ': 'Global X AI & Tech',     # AI/기술 ETF
        'WCLD': 'WisdomTree Cloud',      # 클라우드 컴퓨팅 ETF
    }
    
    for symbol, description in symbols.items():
        try:
            logger.info(f"\nAnalyzing {symbol} ({description})...")
            
            # 데이터 가져오기
            df = collector.get_latest_data(symbol)
            if df.empty:
                logger.warning(f"No data available for {symbol}")
                continue
            
            # 기술적 지표 계산
            indicators = TechnicalIndicators(df)
            
            # 현재 시점의 지표 요약
            summary = indicators.get_summary()
            logger.info("\nCurrent Technical Indicators:")
            for key, value in summary.items():
                logger.info(f"{key}: {value:.2f}")
            
            # 매매 신호 확인
            signals = indicators.get_signals()
            latest_signals = {k: v.iloc[-1] for k, v in signals.items()}
            logger.info("\nLatest Trading Signals:")
            for indicator, signal in latest_signals.items():
                if signal == 1:
                    logger.info(f"{indicator}: BUY")
                elif signal == -1:
                    logger.info(f"{indicator}: SELL")
                else:
                    logger.info(f"{indicator}: NEUTRAL")
            
            # 지표 시각화
            plot_indicators(symbol, indicators.data, indicators)
            
        except Exception as e:
            logger.error(f"Error processing {symbol}: {str(e)}")
            continue

if __name__ == "__main__":
    main() 