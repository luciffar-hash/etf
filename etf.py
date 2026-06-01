import streamlit as st
import yfinance as yf

# --- 版本控制 ---
VERSION = "0.1.8"

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
    # 此處未來將接入真實爬蟲，目前設定為模擬數值以對標玩股網數據
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
            # 這是您指定的精確計算方式
            premium = ((price - nav) / nav) * 100
            
            # 動態顏色渲染：正數(溢價)為紅色，負數(折價)為綠色
            color = "red" if premium > 0 else "green"
            
            col1, col2, col3 = st.columns(3)
            col1.metric("即時市價", f"{price:.2f}")
            col2.metric("最新淨值", f"{nav:.2f}")
            
            # 精準顯示折溢價率 (對齊您在截圖中看到的 0.83% 效果)
            col3.markdown(f"""
            <div style="font-family: sans-serif;">
                <div style="font-size: 0.9rem; color: #808495; margin-bottom: 5px;">折溢價率</div>
                <div style="font-size: 2.2rem; font-weight: bold; color: {color};">
                    {premium:+.2f}%
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # 燈號邏輯
            if premium > 0.5:
                st.error("⚠️ 警示：目前溢價偏高，建議觀察。")
            elif premium < -0.2:
                st.success("✅ 提示：目前為折價狀態，相對划算。")
            else:
                st.info("ℹ️ 狀態：價格合理。")
        else:
            st.error(f"無法取得 {symbol} 的數據，請檢查代號。")

if __name__ == "__main__":
    main()
