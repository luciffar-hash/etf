import streamlit as st
import yfinance as yf
import requests
from bs4 import BeautifulSoup

# --- 版本控制 ---
VERSION = "0.3.0"

# --- 網頁配置 ---
st.set_page_config(page_title="路西法智庫：迦南金鑰", page_icon="🔑", layout="wide")

def get_market_price(ticker_symbol):
    try:
        ticker = yf.Ticker(f"{ticker_symbol}.TW")
        price = ticker.fast_info.last_price
        return round(price, 2) if price else None
    except:
        return None

def get_realtime_nav(ticker_symbol):
    """
    爬蟲實戰：從玩股網獲取該 ETF 的最新淨值
    """
    try:
        url = f"https://wantgoo.com/stock/etf/{ticker_symbol}/discount-premium"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 尋找表格中最新的淨值欄位 (根據玩股網結構)
        # 此處為簡化邏輯，實際運作需確保選擇器能精確捕捉
        table = soup.find('table', {'class': 'table-striped'})
        rows = table.find_all('tr')
        # 獲取第二列 (最新日期) 的第二個數據 (淨值)
        latest_nav = float(rows[1].find_all('td')[2].text.strip())
        return latest_nav
    except:
        return None

def main():
    st.title("🔑 路西法智庫：迦南金鑰")
    st.subheader("Luciffar AI: Canaan Key — ETF NAV Insights")
    st.sidebar.markdown(f"### 系統版本: {VERSION}")
    
    symbol = st.text_input("輸入 ETF 代號 (例如: 0050, 00715L):")
    
    if symbol:
        with st.spinner(f'正在為您擷取 {symbol} 的即時數據...'):
            price = get_market_price(symbol)
            nav = get_realtime_nav(symbol) 
        
        if price and nav:
            diff = price - nav
            premium_pct = (diff / nav) * 100
            
            # 顏色邏輯
            color = "red" if premium_pct > 0 else "green"
            
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("即時市價", f"{price:.2f}")
            c2.metric("最新淨值", f"{nav:.2f}")
            c3.markdown(f"<div style='font-size: 0.9rem; color: #808495;'>折溢價金額</div><div style='font-size: 1.8rem; font-weight: bold; color: {color};'>{diff:+.2f}</div>", unsafe_allow_html=True)
            c4.markdown(f"<div style='font-size: 0.9rem; color: #808495;'>折溢價率</div><div style='font-size: 1.8rem; font-weight: bold; color: {color};'>{premium_pct:+.2f}%</div>", unsafe_allow_html=True)
            
            # 警示機制
            if premium_pct >= 1.0: st.error("⚠️ 高度溢價：買進成本過高，建議避險。")
            elif premium_pct <= -1.0: st.success("✅ 極佳折價：出現明顯折價，具備進場價值！")
            else: st.info("ℹ️ 價格合理：市場交易正常。")
        else:
            st.error("無法自動抓取淨值，請確認代號是否為有效 ETF。")

if __name__ == "__main__":
    main()
