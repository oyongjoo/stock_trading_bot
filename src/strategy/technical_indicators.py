"""
기술적 지표 계산 및 매매 신호 생성 모듈

이 모듈은 주가 데이터를 분석하여 다양한 기술적 지표를 계산하고, 이를 기반으로 매매 신호를 생성합니다.
주요 기능:
1. 이동평균선 (SMA, EMA) 계산
2. RSI (상대강도지수) 계산
3. MACD (이동평균수렴확산지수) 계산
4. 볼린저 밴드 계산
5. 매매 신호 생성

각 지표에 대한 상세 설명:

1. 이동평균선 (Moving Averages)
   - SMA (Simple Moving Average, 단순이동평균선)
     * 일정 기간의 종가를 단순 평균한 값
     * 단기(20일)와 장기(60일) 이동평균선의 교차를 통해 매매 시점 판단
     * 단기선이 장기선을 상향 돌파: 골든크로스 (매수 신호)
     * 단기선이 장기선을 하향 돌파: 데드크로스 (매도 신호)
   
   - EMA (Exponential Moving Average, 지수이동평균선)
     * 최근 데이터에 더 높은 가중치를 부여한 이동평균
     * SMA보다 가격 변동에 더 민감하게 반응
     * 단기 추세 판단에 유용

2. RSI (Relative Strength Index, 상대강도지수)
   - 0~100 사이의 값으로 과매수/과매도 상태를 판단
   - 계산 방법: 일정 기간 동안의 상승폭과 하락폭의 평균을 비교
   - 해석:
     * 70 이상: 과매수 구간 (매도 고려)
     * 30 이하: 과매도 구간 (매수 고려)
     * 50을 기준으로 상승/하락 추세 판단
   - 기본 기간: 14일

3. MACD (Moving Average Convergence Divergence, 이동평균수렴확산지수)
   - 단기(12일)와 장기(26일) EMA의 차이를 이용한 지표
   - 구성 요소:
     * MACD 라인: 단기 EMA - 장기 EMA
     * 시그널 라인: MACD의 9일 이동평균
     * MACD 히스토그램: MACD - 시그널
   - 매매 신호:
     * MACD가 시그널을 상향 돌파: 매수 신호
     * MACD가 시그널을 하향 돌파: 매도 신호
     * 0선 돌파: 추세 전환 신호

4. 볼린저 밴드 (Bollinger Bands)
   - 이동평균선을 중심으로 표준편차를 이용한 상하단 밴드
   - 구성 요소:
     * 중간선: 20일 이동평균
     * 상단밴드: 중간선 + (2 * 표준편차)
     * 하단밴드: 중간선 - (2 * 표준편차)
   - 해석:
     * 상단밴드 터치: 과매수 구간 (매도 고려)
     * 하단밴드 터치: 과매도 구간 (매수 고려)
     * 밴드 폭: 변동성 지표
     * 밴드 수축: 변동성 감소, 큰 움직임 예고
     * 밴드 확장: 변동성 증가

매매 신호 생성 로직:
1. RSI 기반:
   - RSI < 30: 매수 신호
   - RSI > 70: 매도 신호

2. MACD 기반:
   - MACD > 시그널: 매수 신호
   - MACD < 시그널: 매도 신호

3. 볼린저 밴드 기반:
   - 가격 < 하단밴드: 매수 신호
   - 가격 > 상단밴드: 매도 신호

주의사항:
- 단일 지표보다는 여러 지표를 조합하여 사용하는 것이 효과적
- 시장 상황과 거래량을 함께 고려해야 함
- 과거 데이터 기반이므로 100% 정확한 예측은 불가능
- 리스크 관리와 함께 사용해야 함
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional

class TechnicalIndicators:
    def __init__(self, data: pd.DataFrame):
        """
        기술적 지표 계산 클래스
        
        Args:
            data (pd.DataFrame): 주가 데이터 (OHLCV 형식)
        """
        self.data = data.copy()
        self.calculate_all_indicators()
    
    def calculate_all_indicators(self):
        """모든 기술적 지표 계산"""
        self.calculate_moving_averages()
        self.calculate_rsi()
        self.calculate_macd()
        self.calculate_bollinger_bands()
    
    def calculate_moving_averages(self, windows: List[int] = [5, 20, 60, 120]):
        """
        이동평균선 계산
        
        Args:
            windows (List[int]): 이동평균 기간 리스트
        """
        for window in windows:
            self.data[f'SMA_{window}'] = self.data['Close'].rolling(window=window).mean()
            self.data[f'EMA_{window}'] = self.data['Close'].ewm(span=window, adjust=False).mean()
    
    def calculate_rsi(self, window: int = 14):
        """
        RSI(Relative Strength Index) 계산
        
        Args:
            window (int): RSI 계산 기간
        """
        delta = self.data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        
        rs = gain / loss
        self.data['RSI'] = 100 - (100 / (1 + rs))
    
    def calculate_macd(self, fast: int = 12, slow: int = 26, signal: int = 9):
        """
        MACD(Moving Average Convergence Divergence) 계산
        
        Args:
            fast (int): 빠른 이동평균 기간
            slow (int): 느린 이동평균 기간
            signal (int): 시그널 기간
        """
        self.data['EMA_fast'] = self.data['Close'].ewm(span=fast, adjust=False).mean()
        self.data['EMA_slow'] = self.data['Close'].ewm(span=slow, adjust=False).mean()
        self.data['MACD'] = self.data['EMA_fast'] - self.data['EMA_slow']
        self.data['MACD_signal'] = self.data['MACD'].ewm(span=signal, adjust=False).mean()
        self.data['MACD_hist'] = self.data['MACD'] - self.data['MACD_signal']
    
    def calculate_bollinger_bands(self, window: int = 20, num_std: float = 2.0):
        """
        볼린저 밴드 계산
        
        Args:
            window (int): 이동평균 기간
            num_std (float): 표준편차 승수
        """
        self.data['BB_middle'] = self.data['Close'].rolling(window=window).mean()
        std = self.data['Close'].rolling(window=window).std()
        self.data['BB_upper'] = self.data['BB_middle'] + (std * num_std)
        self.data['BB_lower'] = self.data['BB_middle'] - (std * num_std)
    
    def get_signals(self) -> Dict[str, pd.Series]:
        """
        매매 신호 생성
        
        Returns:
            Dict[str, pd.Series]: 각 지표별 매매 신호
        """
        signals = {}
        
        # RSI 기반 신호
        signals['RSI'] = pd.Series(0, index=self.data.index)
        signals['RSI'][self.data['RSI'] < 30] = 1  # 과매도
        signals['RSI'][self.data['RSI'] > 70] = -1  # 과매수
        
        # MACD 기반 신호
        signals['MACD'] = pd.Series(0, index=self.data.index)
        signals['MACD'][self.data['MACD'] > self.data['MACD_signal']] = 1  # 골든크로스
        signals['MACD'][self.data['MACD'] < self.data['MACD_signal']] = -1  # 데드크로스
        
        # 볼린저 밴드 기반 신호
        signals['BB'] = pd.Series(0, index=self.data.index)
        signals['BB'][self.data['Close'] < self.data['BB_lower']] = 1  # 하단 돌파
        signals['BB'][self.data['Close'] > self.data['BB_upper']] = -1  # 상단 돌파
        
        return signals
    
    def get_summary(self) -> Dict[str, float]:
        """
        현재 시점의 기술적 지표 요약
        
        Returns:
            Dict[str, float]: 현재 시점의 주요 지표값
        """
        latest = self.data.iloc[-1]
        return {
            'Close': latest['Close'],
            'RSI': latest['RSI'],
            'MACD': latest['MACD'],
            'MACD_signal': latest['MACD_signal'],
            'BB_upper': latest['BB_upper'],
            'BB_middle': latest['BB_middle'],
            'BB_lower': latest['BB_lower'],
            'SMA_20': latest['SMA_20'],
            'SMA_60': latest['SMA_60']
        } 