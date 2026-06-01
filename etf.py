import streamlit as st
import yfinance as yf

# --- 版本控制 ---
VERSION = "0.2.2"

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
    # 模擬數據
    return 104.67 

def get_status_msg(premium):
    """
    更新顏色判定邏輯：溢價為黃色至紅色梯度，折價為綠色。
    """
    if premium >= 1.0:
        return "⚠️ 高度溢價 (>=1%)：買進成本過高，建議避險。", "error", "red"
    elif premium > 0:
        return "⚡ 輕微溢價：市場價格略高於淨值，請審慎評估。", "warning", "orange"
    elif premium <= -1.0:
        return "✅ 極佳折價 (<= -1%)：出現明顯折價，具備進場價值！", "success", "green"
    else:
        return "ℹ️ 輕微折價：目前價格略低於淨值。", "info", "blue"

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
            diff = price - nav
            premium_pct = (diff / nav) * 100
            
            # 獲取顏色與訊息
            msg, msg_type, color_code = get_status_msg(premium_pct)
            
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("即時市價", f"{price:.2f}")
            c2.metric("最新淨值", f"{nav:.2f}")
            
            # 顯示區使用動態顏色
            c3.markdown(f"<div style='font-size: 0.9rem; color: #808495;'>折溢價金額</div><div style='font-size: 1.8rem; font-weight: bold; color: {color_code};'>{diff:+.2f}</div>", unsafe_allow_html=True)
            c4.markdown(f"<div style='font-size: 0.9rem; color: #808495;'>折溢價率</div><div style='font-size: 1.8rem; font-weight: bold; color: {color_code};'>{premium_pct:+.2f}%</div>", unsafe_allow_html=True)
            
            # 狀態回饋
            if msg_type == "error": st.error(msg)
            elif msg_type == "warning": st.warning(msg)
            elif msg_type == "success": st.success(msg)
            else: st.info(msg)
        else:
            st.error(f"無法取得 {symbol} 的數據，請檢查代號。")

if __name__ == "__main__":
    main()
