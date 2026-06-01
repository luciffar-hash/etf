import streamlit as st
import pandas as pd

# --- 版本控制 ---
VERSION = "0.1.1"

# --- 網頁配置 ---
st.set_page_config(
    page_title="路西法智庫：迦南金鑰",
    page_icon="🔑",
    layout="wide"
)

def calculate_premium_discount(market_price, nav):
    """
    精確計算折溢價率
    公式：((市價 - 淨值) / 淨值) * 100
    """
    if nav == 0:
        return 0.0
    premium_rate = ((market_price - nav) / nav) * 100
    return round(premium_rate, 2)

def main():
    # --- 頁面標題與版號 ---
    st.title("🔑 路西法智庫：迦南金鑰")
    st.subheader("Luciffar AI: Canaan Key — ETF NAV Insights")
    
    # 側邊欄顯示版號
    st.sidebar.markdown(f"### 系統版本: {VERSION}")
    st.sidebar.info("路西法智庫，洞悉市場真理。")

    # --- 核心功能區 ---
    st.markdown("---")
    
    # 模擬資料輸入區 (後續將改為自動爬取)
    col1, col2, col3 = st.columns(3)
    with col1:
        market_price = st.number_input("輸入市價:", min_value=0.0, format="%.2f")
    with col2:
        nav = st.number_input("輸入淨值:", min_value=0.0, format="%.2f")
    
    if st.button("計算折溢價"):
        if nav > 0:
            rate = calculate_premium_discount(market_price, nav)
            st.metric(label="即時折溢價率", value=f"{rate}%")
            
            # 邏輯判斷：紅色警告或綠色划算
            if rate > 1.0:
                st.error("⚠️ 警示：目前溢價過高，買進需謹慎！")
            elif rate < -0.5:
                st.success("✅ 提示：目前為折價狀態，相對划算。")
            else:
                st.info("ℹ️ 狀態：價格合理。")
        else:
            st.error("淨值不能為 0")

if __name__ == "__main__":
    main()
