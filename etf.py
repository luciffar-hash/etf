import streamlit as st
import yfinance as yf

# --- 版本控制 ---
VERSION = "0.1.9"

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
    # 模擬數據：未來將對接自動爬蟲
    return 104.67 

def main():
    st.title("🔑 路西法智庫：迦南金鑰")
    st.subheader("Luciffar AI: Canaan Key — ETF NAV Insights")
    st.sidebar.markdown(f"### 系統版本: {VERSION}")
    
    st.write("---")
    symbol = st.text_input("輸入 ETF 代號 (例如: 0050, 00631L):")
    
    if symbol:
        with st.spinner('正在更新市場數據...'):
            price = get_market_price(symbol)
            nav = get_latest_nav(symbol) 
        
        if price and nav:
            # 計算數據
            diff = price - nav  # 折溢價金額
            premium_pct = (diff / nav) * 100 # 折溢價率
            
            # 顏色判定邏輯
            color = "red" if diff > 0 else "green"
            
            # 擴充為四欄位顯示
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("即時市價", f"{price:.2f}")
            c2.metric("最新淨值", f"{nav:.2f}")
            
            # 折溢價金額顯示 (新增欄位)
            c3.markdown(f"""
            <div style="font-family: sans-serif;">
                <div style="font-size: 0.9rem; color: #808495; margin-bottom: 5px;">折溢價金額</div>
                <div style="font-size: 1.8rem; font-weight: bold; color: {color};">
                    {diff:+.2f}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # 折溢價率顯示
            c4.markdown(f"""
            <div style="font-family: sans-serif;">
                <div style="font-size: 0.9rem; color: #808495; margin-bottom: 5px;">折溢價率</div>
                <div style="font-size: 1.8rem; font-weight: bold; color: {color};">
                    {premium_pct:+.2f}%
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # 燈號邏輯
            if diff > 0.5:
                st.error("⚠️ 警示：目前溢價偏高，建議觀察。")
            elif diff < -0.2:
                st.success("✅ 提示：目前為折價狀態，相對划算。")
            else:
                st.info("ℹ️ 狀態：價格合理。")
        else:
            st.error(f"無法取得 {symbol} 的數據，請檢查代號。")

if __name__ == "__main__":
    main()
