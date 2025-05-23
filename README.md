# Stock Trading Bot

자동 주식 거래 봇 프로젝트입니다.

## 프로젝트 개요
이 프로젝트는 외국주식 자동매매를 위한 트레이딩 봇입니다. Python을 기반으로 하여 실시간 시장 데이터를 분석하고 자동으로 매매를 실행합니다.

## 주요 기능
- 실시간 시장 데이터 수집 및 분석
- 다양한 트레이딩 전략 구현
- 자동 주문 실행 및 포지션 관리
- 백테스팅을 통한 전략 검증
- 실시간 모니터링 및 알림

## 프로젝트 구조
```
stock_trading_bot/
├── config/                 # 설정 파일
├── data/                   # 데이터 저장
│   ├── market_data/       # 시장 데이터
│   └── backtest_results/  # 백테스팅 결과
├── src/                    # 소스 코드
│   ├── data/              # 데이터 수집 및 처리
│   ├── strategy/          # 트레이딩 전략
│   ├── trading/           # 주문 실행 및 관리
│   └── utils/             # 유틸리티 함수
└── tests/                 # 테스트 코드
```

## 개발 일지

### 2024-03-21
- 프로젝트 초기 구조 설정
- 기본 디렉토리 구조 생성
- README.md 작성

## 설치 및 실행 방법
(추후 업데이트 예정)

## 사용된 주요 라이브러리
- yfinance: Yahoo Finance API
- pandas: 데이터 분석
- numpy: 수치 계산
- backtrader: 백테스팅
- TA-Lib: 기술적 지표
- (추후 업데이트 예정)

## 개발 예정 사항
1. 기본 데이터 수집 모듈 구현
2. 간단한 트레이딩 전략 구현
3. 백테스팅 시스템 구축
4. 실시간 트레이딩 시스템 구현
5. 모니터링 및 알림 시스템 구축

## 주의사항
- 이 프로그램은 실제 투자에 사용하기 전에 충분한 테스트가 필요합니다.
- 투자에 따른 손실은 사용자의 책임입니다.
- API 키와 같은 민감한 정보는 반드시 안전하게 관리해야 합니다. 

## 주요 기능

### 1. 데이터 수집
- yfinance를 사용한 실시간 주가 데이터 수집
- 일별 자동 데이터 수집 (18:00 ET)
- 수집 데이터: OHLCV (시가, 고가, 저가, 종가, 거래량)

### 2. 기술적 분석
현재 분석 가능한 종목:

#### AI/반도체 관련
- NVDA (NVIDIA): AI 반도체 선두주
- AMD: AI 반도체 경쟁사
- INTC (Intel): 반도체 제조
- AVGO (Broadcom): AI 네트워킹 칩
- MU (Micron): AI 메모리

#### AI 소프트웨어/서비스
- MSFT (Microsoft): AI 클라우드/소프트웨어
- GOOGL (Google): AI 검색/클라우드
- META (Meta): AI 소셜미디어
- CRM (Salesforce): AI 기업용 소프트웨어
- PLTR (Palantir): AI 데이터 분석

#### 전기차/배터리
- TSLA (Tesla): 전기차 선두주
- RIVN (Rivian): 전기차 신흥주
- LCID (Lucid): 전기차 신흥주
- QS (QuantumScape): 차세대 배터리
- ENVX (Enovix): 차세대 배터리

#### ESS/재생에너지
- ENPH (Enphase): 태양광 인버터
- SEDG (SolarEdge): 태양광 인버터
- RUN (Sunrun): 태양광 설치
- STEM: 에너지 저장
- BE (Bloom Energy): 수소 연료전지

#### AI/로봇 관련 ETF
- BOTZ: Global Robotics & AI ETF
- ARKQ: ARK Autonomous Tech ETF
- ROBO: Robo Global Robotics ETF
- AIQ: Global X AI & Tech ETF
- WCLD: WisdomTree Cloud ETF

### 3. 기술적 지표
각 종목에 대해 다음 기술적 지표를 계산하고 분석합니다:

#### 이동평균선 (Moving Averages)
- SMA (Simple Moving Average, 단순이동평균선)
  * 20일, 60일 이동평균선
  * 골든크로스/데드크로스 분석
- EMA (Exponential Moving Average, 지수이동평균선)
  * 최근 데이터에 가중치 부여
  * 단기 추세 분석

#### RSI (Relative Strength Index, 상대강도지수)
- 0~100 사이의 값으로 과매수/과매도 상태 판단
- 14일 기준
- 매매 신호:
  * RSI < 30: 과매도 (매수 고려)
  * RSI > 70: 과매수 (매도 고려)

#### MACD (Moving Average Convergence Divergence)
- 12일, 26일 EMA 기반
- 구성 요소:
  * MACD 라인: 단기 EMA - 장기 EMA
  * 시그널 라인: MACD의 9일 이동평균
  * MACD 히스토그램: MACD - 시그널
- 매매 신호:
  * MACD > 시그널: 매수 신호
  * MACD < 시그널: 매도 신호

#### 볼린저 밴드 (Bollinger Bands)
- 20일 이동평균선 기준
- 구성 요소:
  * 중간선: 20일 이동평균
  * 상단밴드: 중간선 + (2 * 표준편차)
  * 하단밴드: 중간선 - (2 * 표준편차)
- 매매 신호:
  * 가격 < 하단밴드: 매수 신호
  * 가격 > 상단밴드: 매도 신호

### 4. 시각화
각 종목별로 다음 차트를 생성합니다:
1. 가격 차트와 이동평균선
   - 종가
   - 20일 SMA
   - 60일 SMA
   - 볼린저 밴드
2. RSI 차트
   - RSI 라인
   - 30/70 기준선
3. MACD 차트
   - MACD 라인
   - 시그널 라인
   - MACD 히스토그램

차트는 `data/backtest_results/` 디렉토리에 저장됩니다.

## 사용 방법

### 환경 설정
```bash
# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 또는
.\venv\Scripts\activate  # Windows

# 필요한 패키지 설치
pip install -r requirements.txt
```

### 데이터 수집 실행
```bash
python src/data/scheduler.py
```

### 기술적 분석 실행
```bash
python src/strategy/test_indicators.py
```

## 주의사항
- 단일 지표보다는 여러 지표를 조합하여 사용하는 것이 효과적
- 시장 상황과 거래량을 함께 고려해야 함
- 과거 데이터 기반이므로 100% 정확한 예측은 불가능
- 리스크 관리와 함께 사용해야 함

## 로깅
- 모든 분석 결과는 로그 파일에 기록됩니다
- 에러 발생 시 상세한 에러 메시지가 기록됩니다
- 차트 저장 경로와 상태가 로그에 기록됩니다 