"""
주식 데이터 웹 대시보드

이 모듈은 수집된 주식 데이터를 웹 대시보드로 시각화합니다.
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from flask import Flask, render_template, jsonify
from src.data.data_collector import StockDataCollector
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from datetime import datetime

app = Flask(__name__)
collector = StockDataCollector()

def create_stock_chart(symbol: str, df: pd.DataFrame) -> dict:
    """주식 차트 생성"""
    fig = make_subplots(rows=3, cols=1, 
                       shared_xaxes=True,
                       vertical_spacing=0.05,
                       row_heights=[0.6, 0.2, 0.2])

    # 가격 차트
    fig.add_trace(go.Candlestick(x=df.index,
                                open=df['Open'],
                                high=df['High'],
                                low=df['Low'],
                                close=df['Close'],
                                name='OHLC'),
                  row=1, col=1)

    # 이동평균선
    fig.add_trace(go.Scatter(x=df.index, y=df['SMA_20'],
                            name='SMA 20',
                            line=dict(color='blue')),
                  row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['SMA_60'],
                            name='SMA 60',
                            line=dict(color='red')),
                  row=1, col=1)

    # RSI
    fig.add_trace(go.Scatter(x=df.index, y=df['RSI'],
                            name='RSI',
                            line=dict(color='purple')),
                  row=2, col=1)
    fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
    fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)

    # MACD
    fig.add_trace(go.Scatter(x=df.index, y=df['MACD'],
                            name='MACD',
                            line=dict(color='blue')),
                  row=3, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['MACD_signal'],
                            name='Signal',
                            line=dict(color='red')),
                  row=3, col=1)
    fig.add_trace(go.Bar(x=df.index, y=df['MACD_hist'],
                        name='Histogram',
                        marker_color='gray'),
                  row=3, col=1)

    # 레이아웃 설정
    fig.update_layout(
        title=f'{symbol} Technical Analysis',
        yaxis_title='Price',
        yaxis2_title='RSI',
        yaxis3_title='MACD',
        xaxis_rangeslider_visible=False,
        height=800
    )

    return json.loads(fig.to_json())

@app.route('/')
def index():
    """메인 페이지"""
    return render_template('index.html', symbols=collector.symbols)

@app.route('/api/stock/<symbol>')
def get_stock_data(symbol):
    """주식 데이터 API"""
    try:
        # 데이터 가져오기
        df = collector.get_latest_data(symbol)
        if df.empty:
            return jsonify({'error': 'No data available'}), 404

        # 기술적 지표 계산
        from src.strategy.technical_indicators import TechnicalIndicators
        indicators = TechnicalIndicators(df)
        
        # 차트 데이터 생성
        chart_data = create_stock_chart(symbol, indicators.data)
        
        # 종목 정보 가져오기
        info = collector.get_symbol_info(symbol)
        
        # 최신 가격 정보
        latest = indicators.data.iloc[-1]
        price_info = {
            'close': latest['Close'],
            'change': latest['Close'] - indicators.data.iloc[-2]['Close'],
            'change_percent': ((latest['Close'] - indicators.data.iloc[-2]['Close']) / indicators.data.iloc[-2]['Close']) * 100,
            'volume': latest['Volume']
        }
        
        # 기술적 지표 요약
        summary = indicators.get_summary()
        
        # 매매 신호
        signals = indicators.get_signals()
        latest_signals = {k: v.iloc[-1] for k, v in signals.items()}
        
        return jsonify({
            'chart': chart_data,
            'info': info,
            'price': price_info,
            'indicators': summary,
            'signals': latest_signals
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/update_all')
def update_all_data():
    """모든 종목 데이터 업데이트"""
    try:
        collector.collect_all_data()
        return jsonify({'message': 'Data updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 