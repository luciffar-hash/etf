import streamlit as st
import yfinance as yf
import pandas as pd

# --- 版本控制 ---
VERSION = "0.1.3"

# --- 網頁配置 ---
st.set_page_config(page_title="路西法智庫：迦南金鑰", page_icon="🔑", layout="wide")

def get_market_price(ticker_symbol):
    """
    從 Yahoo Finance 獲取即時報價
    台股代號需加上 .TW (例如 0050.TW)
    """
    try:
        ticker = yf.Ticker(f"{ticker_symbol}.TW")
        data = ticker.history(period="1d")
        if not data.empty:
            return round(data['Close'].iloc[-1], 2)
        return None
    except:
        return None

def main():
    st.title("🔑 路西法智庫：迦南金鑰")
    st.subheader("Luciffar AI: Canaan Key — ETF NAV Insights")
    st.sidebar.markdown(f"### 系統版本: {VERSION}")
    
    tab1, tab2 = st.tabs(["📊 即時監控", "📋 監控清單"])
    
    with tab1:
        st.write("### 自動報價系統")
        symbol = st.text_input("輸入 ETF 代號 (例如: 0050, 00631L):")
        
        if symbol:
            price = get_market_price(symbol)
            if price:
                st.success(f"目前市價: {price}")
                nav = st.number_input("手動輸入最新淨值 (NAV) 以計算溢價:", min_value=0.0, format="%.2f")
                if nav > 0:
                    premium = ((price - nav) / nav) * 100
                    st.metric("即時折溢價率", f"{round(premium, 2)}%")
            else:
                st.error("無法取得報價，請確認代號是否正確。")

    with tab2:
        st.write("### 監控清單")
        st.info("系統已準備好串接多個標的，下一步將實作自動化列表追蹤。")

if __name__ == "__main__":
    main()
