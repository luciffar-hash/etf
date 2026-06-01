import streamlit as st
import yfinance as yf

# --- 版本控制 ---
VERSION = "0.1.4"

# --- 網頁配置 ---
st.set_page_config(page_title="路西法智庫：迦南金鑰", page_icon="🔑", layout="wide")

def get_market_price(ticker_symbol):
    """
    優化後的報價抓取函數
    """
    try:
        # 確保代號正確格式
        ticker_str = f"{ticker_symbol}.TW"
        ticker = yf.Ticker(ticker_str)
        # 使用 fast_info 獲取更即時的資訊
        price = ticker.fast_info.last_price
        return round(price, 2) if price else None
    except Exception as e:
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
            with st.spinner('正在查詢市場數據...'):
                price = get_market_price(symbol)
            
            if price:
                st.success(f"目前市價: {price}")
                nav = st.number_input("手動輸入最新淨值 (NAV) 以計算溢價:", min_value=0.0, format="%.2f")
                if nav > 0:
                    premium = ((price - nav) / nav) * 100
                    st.metric("即時折溢價率", f"{round(premium, 2)}%")
            else:
                st.error(f"無法取得 {symbol}.TW 的報價，請檢查代號或網路連線。")

    with tab2:
        st.write("### 監控清單")
        st.info("系統已準備好串接多個標的。")

if __name__ == "__main__":
    main()
