import streamlit as st
import yfinance as yf

# --- 版本控制 ---
VERSION = "0.4.3"

# --- 網頁配置 ---
st.set_page_config(page_title="路西法智庫：迦南金鑰", page_icon="🔑", layout="wide")

def get_market_price(ticker_symbol):
    try:
        ticker = yf.Ticker(f"{ticker_symbol}.TW")
        price = ticker.fast_info.last_price
        return round(price, 2) if price and price > 0 else None
    except:
        return None

def main():
    st.title("🔑 路西法智庫：迦南金鑰")
    st.subheader("Luciffar AI: Canaan Key — ETF NAV Insights")
    
    symbol = st.text_input("輸入 ETF 代號 (例如: 0050, 00715L):")
    
    # 使用 placeholder 固定版面位置
    placeholder = st.empty()
    
    if symbol:
        price = get_market_price(symbol)
        # 暫時維持模擬數值以固定介面顯示
        nav = 104.67 if symbol == "0050" else 52.60
        
        with placeholder.container():
            if price:
                diff = price - nav
                pct = (diff / nav) * 100
                color = "red" if diff > 0 else "green"
                
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("即時市價", f"{price:.2f}")
                c2.metric("最新淨值", f"{nav:.2f}")
                
                # 強制使用 HTML 確保字體與間距統一
                c3.markdown(f"<div style='font-size: 0.9rem; color: #808495;'>折溢價金額</div><div style='font-size: 1.8rem; font-weight: bold; color: {color};'>{diff:+.2f}</div>", unsafe_allow_html=True)
                c4.markdown(f"<div style='font-size: 0.9rem; color: #808495;'>折溢價率</div><div style='font-size: 1.8rem; font-weight: bold; color: {color};'>{pct:+.2f}%</div>", unsafe_allow_html=True)
                
                if pct >= 1.0: st.error("⚠️ 高度溢價 (>=1%)：買進成本過高，建議避險。")
                elif pct <= -1.0: st.success("✅ 極佳折價 (<= -1%)：出現明顯折價，具備進場價值！")
                else: st.info("ℹ️ 價格合理：市場交易正常。")
            else:
                st.warning(f"⚠️ 正在嘗試獲取 {symbol} 的市場數據，請稍候...")

if __name__ == "__main__":
    main()
