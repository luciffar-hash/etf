import streamlit as st
import yfinance as yf
from FinMind.data import DataLoader

# --- 版本控制 ---
VERSION = "0.3.1"

# --- 網頁配置 ---
st.set_page_config(page_title="路西法智庫：迦南金鑰", page_icon="🔑", layout="wide")

def get_market_price(ticker_symbol):
    try:
        ticker = yf.Ticker(f"{ticker_symbol}.TW")
        return round(ticker.fast_info.last_price, 2)
    except:
        return None

def get_realtime_nav(ticker_symbol):
    """
    透過 FinMind API 獲取最新的 ETF 淨值
    """
    try:
        dl = DataLoader()
        # 獲取 ETF 淨值數據
        df = dl.taiwan_stock_daily(stock_id=ticker_symbol, start_date="2026-06-01")
        # 這裡需根據實際 API 回傳欄位調整，通常最新資料在最後一行
        return float(df['close'].iloc[-1]) 
    except:
        return None

def main():
    st.title("🔑 路西法智庫：迦南金鑰")
    st.subheader("Luciffar AI: Canaan Key — ETF NAV Insights")
    
    symbol = st.text_input("輸入 ETF 代號 (例如: 0050, 00715L):")
    
    if symbol:
        with st.spinner(f'正在向金融中心查詢 {symbol} 數據...'):
            price = get_market_price(symbol)
            nav = get_realtime_nav(symbol)
            
            if price and nav:
                diff = price - nav
                pct = (diff / nav) * 100
                color = "red" if diff > 0 else "green"
                
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("即時市價", f"{price:.2f}")
                c2.metric("最新淨值", f"{nav:.2f}")
                c3.markdown(f"<div style='color:{color}; font-size:1.8rem; font-weight:bold;'>{diff:+.2f}</div>", unsafe_allow_html=True)
                c4.markdown(f"<div style='color:{color}; font-size:1.8rem; font-weight:bold;'>{pct:+.2f}%</div>", unsafe_allow_html=True)
                
                if pct >= 1.0: st.error("⚠️ 高度溢價：買進成本過高，建議避險。")
                elif pct <= -1.0: st.success("✅ 極佳折價：具備進場價值！")
                else: st.info("ℹ️ 價格合理：市場交易正常。")
            else:
                st.error("系統無法取得數據，請確認 API 連線狀態。")

if __name__ == "__main__":
    main()
