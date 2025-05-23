"""
주식 데이터 수집 모듈

이 모듈은 yfinance를 사용하여 주식 데이터를 수집하고 저장합니다.
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import logging
import os
import time

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class StockDataCollector:
    def __init__(self):
        """데이터 수집기 초기화"""
        self.symbols = {
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
        
        # 데이터 저장 디렉토리 생성
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'market_data')
        os.makedirs(self.data_dir, exist_ok=True)
        
        # 종목 정보 캐시 초기화
        self.info_cache = {}
    
    def get_latest_data(self, symbol: str, period: str = '1y') -> pd.DataFrame:
        """
        최신 주가 데이터 수집 또는 로드
        우선 로컬 CSV 파일에서 데이터를 로드하고, 없으면 yfinance로 수집합니다.
        
        Args:
            symbol (str): 주식 심볼
            period (str): 데이터 기간 (기본값: 1년)
        
        Returns:
            pd.DataFrame: 주가 데이터
        """
        # 로컬 파일 경로 설정 (예: data/market_data/NVDA_1d_20250523.csv)
        today_str = datetime.now().strftime('%Y%m%d')
        filename = f"{symbol}_1d_{today_str}.csv"
        filepath = os.path.join(self.data_dir, filename)

        # 로컬 파일에서 데이터 로드 시도
        if os.path.exists(filepath):
            try:
                logger.info(f"Loading data for {symbol} from local file {filepath}")
                df = pd.read_csv(filepath, index_col=0, parse_dates=True)
                if not df.empty:
                    logger.info(f"Successfully loaded data for {symbol} from local file.")
                    # 최신 가격 로깅 (로컬 파일에서 로드 시)
                    latest_price = df['Close'].iloc[-1]
                    logger.info(f"Latest price for {symbol} (from file): ${latest_price:.2f}")
                    return df
                else:
                    logger.warning(f"Local file {filepath} is empty for {symbol}.")
            except Exception as e:
                logger.error(f"Error loading data from local file {filepath}: {str(e)}")
        
        # 로컬 파일 로드 실패 또는 파일 부재 시 yfinance로 데이터 수집
        try:
            logger.info(f"Fetching data for {symbol} from yfinance for {period}")
            stock = yf.Ticker(symbol)
            df = stock.history(period=period)
            
            if not df.empty:
                # 데이터 저장
                df.to_csv(filepath)
                logger.info(f"Data saved to {filepath}")
                
                # 최신 가격 로깅
                latest_price = df['Close'].iloc[-1]
                logger.info(f"Latest price for {symbol} (from yfinance): ${latest_price:.2f}")
            else:
                 logger.warning(f"No data found for {symbol} from yfinance for {period}.")
            
            return df
            
        except Exception as e:
            logger.error(f"Error fetching data for {symbol} from yfinance: {str(e)}")
            return pd.DataFrame()
        finally:
            # API 호출 후 짧은 대기 시간 추가
            time.sleep(1) # 1초 대기
    
    def collect_all_data(self):
        """모든 종목의 데이터 수집"""
        for symbol, description in self.symbols.items():
            logger.info(f"\nCollecting data for {symbol} ({description})...")
            self.get_latest_data(symbol)
            # 데이터 수집 시 종목 정보도 미리 가져와 캐시에 저장
            self.get_symbol_info(symbol)
    
    def get_symbol_info(self, symbol: str) -> dict:
        """
        종목 정보 조회 (캐시 사용)
        
        Args:
            symbol (str): 주식 심볼
        
        Returns:
            dict: 종목 정보
        """
        # 캐시에 정보가 있으면 반환
        if symbol in self.info_cache:
            logger.info(f"Loading info for {symbol} from cache.")
            return self.info_cache[symbol]

        # 캐시에 없으면 yfinance로 가져와서 캐시에 저장 후 반환
        try:
            logger.info(f"Fetching info for {symbol} from yfinance.")
            stock = yf.Ticker(symbol)
            info = stock.info
            symbol_info = {
                'name': info.get('longName', ''),
                'sector': info.get('sector', ''),
                'industry': info.get('industry', ''),
                'market_cap': info.get('marketCap', 0),
                'pe_ratio': info.get('trailingPE', 0),
                'dividend_yield': info.get('dividendYield', 0),
                'beta': info.get('beta', 0)
            }
            self.info_cache[symbol] = symbol_info
            logger.info(f"Successfully fetched and cached info for {symbol}.")
            return symbol_info
        except Exception as e:
            logger.error(f"Error fetching info for {symbol} from yfinance: {str(e)}")
            # 오류 발생 시에도 빈 딕셔너리를 캐시에 저장하여 불필요한 재시도 방지
            self.info_cache[symbol] = {}
            return {}
        finally:
            # API 호출 후 짧은 대기 시간 추가
            time.sleep(1) # 1초 대기 