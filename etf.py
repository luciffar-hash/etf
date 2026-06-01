import streamlit as st
import yfinance as yf

# --- 版本控制 ---
VERSION = "0.1.5"

# --- 網頁配置 ---
st.set_page_config(page_title="路西法智庫：迦南金鑰", page_icon="🔑", layout="wide")

def get_market_price(ticker_symbol):
    try:
        ticker = yf.Ticker(f"{ticker_symbol}.TW")
        price = ticker.fast_info.last_price
        return round(price, 2) if price else None
    except:
        return None

def get_latest_nav(ticker_symbol):
    """
    未來這裡將接入自動爬蟲邏輯
    目前先預留，避免程式錯誤
    """
    # 這裡未來會串接各投信官網或證交所 API
    return 105.0 # 暫時模擬數值，供您測試介面

def main():
    st.title("🔑 路西法智庫：迦南金鑰")
    st.subheader("Luciffar AI: Canaan Key — ETF NAV Insights")
    st.sidebar.markdown(f"### 系統版本: {VERSION}")
    
    st.write("---")
    symbol = st.text_input("輸入 ETF 代號 (例如: 0050, 00631L):")
    
    if symbol:
        with st.spinner('正在從迦南金鑰擷取市場數據...'):
            price = get_market_price(symbol)
            nav = get_latest_nav(symbol) # 自動獲取淨值
        
        if price and nav:
            premium = ((price - nav) / nav) * 100
            
            # 顯示結果區
            col1, col2, col3 = st.columns(3)
            col1.metric("即時市價", price)
            col2.metric("最新淨值", nav)
            col3.metric("折溢價率", f"{round(premium, 2)}%")
            
            # 燈號邏輯
            if premium > 1.0:
                st.error("⚠️ 警示：目前溢價過高，買進需謹慎！")
            elif premium < -0.5:
                st.success("✅ 提示：目前為折價狀態，相對划算。")
            else:
                st.info("ℹ️ 狀態：價格合理。")
        else:
            st.error(f"無法取得 {symbol} 的完整數據，請檢查代號。")

if __name__ == "__main__":
    main()
