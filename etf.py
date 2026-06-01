import streamlit as st
import yfinance as yf

# --- 版本控制 ---
VERSION = "0.1.6"

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
    未來這裡將接入正式爬蟲API。
    目前為了精確呈現，我們將預留浮點數處理邏輯。
    """
    # 模擬 0050 的精確淨值 104.67
    return 104.67 

def main():
    st.title("🔑 路西法智庫：迦南金鑰")
    st.subheader("Luciffar AI: Canaan Key — ETF NAV Insights")
    st.sidebar.markdown(f"### 系統版本: {VERSION}")
    
    st.write("---")
    symbol = st.text_input("輸入 ETF 代號 (例如: 0050, 00631L):")
    
    if symbol:
        with st.spinner('正在從迦南金鑰擷取精確數據...'):
            price = get_market_price(symbol)
            nav = get_latest_nav(symbol) 
        
        if price and nav:
            # 精確計算：使用 round(val, 2) 確保顯示至小數點後兩位
            premium = ((price - nav) / nav) * 100
            
            # 使用 formatted string {: .2f} 確保數值顯示精確到小數點後兩位
            col1, col2, col3 = st.columns(3)
            col1.metric("即時市價", f"{price:.2f}")
            col2.metric("最新淨值", f"{nav:.2f}")
            col3.metric("折溢價率", f"{premium:.2f}%")
            
            # 燈號邏輯
            if premium > 1.0:
                st.error("⚠️ 警示：目前溢價過高，買進需謹慎！")
            elif premium < -0.5:
                st.success("✅ 提示：目前為折價狀態，相對划算。")
            else:
                st.info("ℹ️ 狀態：價格合理。")
        else:
            st.error(f"無法取得 {symbol} 的數據，請檢查代號。")

if __name__ == "__main__":
    main()
