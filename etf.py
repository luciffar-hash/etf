import streamlit as st
import yfinance as yf

# --- 版本控制 ---
VERSION = "0.4.1"

# --- 網頁配置 ---
st.set_page_config(page_title="路西法智庫：迦南金鑰", page_icon="🔑", layout="wide")

def get_market_price(ticker_symbol):
    """
    加入容錯機制：若標準 .TW 抓不到，嘗試不加後綴或檢查該代號
    """
    possible_symbols = [f"{ticker_symbol}.TW", ticker_symbol]
    for sym in possible_symbols:
        try:
            ticker = yf.Ticker(sym)
            # 使用 fast_info 獲取最新價格
            price = ticker.fast_info.last_price
            if price and price > 0:
                return round(price, 2)
        except:
            continue
    return None

def get_latest_nav(ticker_symbol):
    # 此處仍需正式對接，目前先保持邏輯架構
    return 104.67 

def main():
    st.title("🔑 路西法智庫：迦南金鑰")
    symbol = st.text_input("輸入 ETF 代號 (例如: 0050, 00715L):")
    
    if symbol:
        price = get_market_price(symbol)
        nav = get_latest_nav(symbol)
        
        if price:
            st.success(f"系統已成功抓取 {symbol} 市價: {price}")
            # ... (後續顯示邏輯同前)
        else:
            st.error(f"無法取得 {symbol} 報價，請檢查代號或確認是否為台股上市公司。")

if __name__ == "__main__":
    main()
