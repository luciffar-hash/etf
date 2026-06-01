import streamlit as st

# --- 版本控制 ---
VERSION = "0.1.2"

# --- 網頁配置 ---
st.set_page_config(
    page_title="路西法智庫：迦南金鑰",
    page_icon="🔑",
    layout="wide"
)

def calculate_premium_discount(market_price, nav):
    """
    精確計算折溢價率
    """
    if nav <= 0:
        return 0.0
    premium_rate = ((market_price - nav) / nav) * 100
    return round(premium_rate, 2)

def main():
    # --- 頁面標題與版號 ---
    st.title("🔑 路西法智庫：迦南金鑰")
    st.subheader("Luciffar AI: Canaan Key — ETF NAV Insights")
    st.sidebar.markdown(f"### 系統版本: {VERSION}")
    st.sidebar.info("路西法智庫，洞悉市場真理。")

    # --- 核心邏輯區 ---
    tab1, tab2 = st.tabs(["📊 即時計算器", "📋 監控清單預覽"])
    
    with tab1:
        st.write("### 快速折溢價試算")
        col1, col2 = st.columns(2)
        with col1:
            market_price = st.number_input("輸入市價 (Market Price):", min_value=0.0, format="%.2f")
        with col2:
            nav = st.number_input("輸入淨值 (NAV):", min_value=0.0, format="%.2f")
        
        if st.button("執行計算"):
            if nav > 0:
                rate = calculate_premium_discount(market_price, nav)
                st.metric(label="即時折溢價率", value=f"{rate}%")
                if rate > 1.0:
                    st.error("⚠️ 警示：目前溢價過高，買進需謹慎！")
                elif rate < -0.5:
                    st.success("✅ 提示：目前為折價狀態，相對划算。")
                else:
                    st.info("ℹ️ 狀態：價格合理。")
            else:
                st.error("淨值數值異常，請確認輸入。")

    with tab2:
        st.write("### 預定監控清單")
        st.write("系統將自動追蹤以下標的 (開發中...):")
        etf_list = ["0050", "00631L", "00830", "00735"]
        st.table({"ETF 代號": etf_list, "狀態": ["待建置"] * len(etf_list)})

if __name__ == "__main__":
    main()
