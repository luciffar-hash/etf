import streamlit as st

# --- 版本控制 ---
VERSION = "0.1.0"

# --- 網頁配置 ---
st.set_page_config(
    page_title="路西法智庫：迦南金鑰",
    page_icon="🔑",
    layout="wide"
)

def main():
    # --- 頁面標題與版號 ---
    st.title("🔑 路西法智庫：迦南金鑰")
    st.subheader("Luciffar AI: Canaan Key — ETF NAV Insights")
    
    # 側邊欄顯示版號
    st.sidebar.markdown(f"### 系統版本: {VERSION}")
    st.sidebar.info("路西法智庫，洞悉市場真理。")

    # --- 核心功能區 ---
    st.markdown("---")
    st.write("系統已啟動。")
    st.write("目前版本主要功能：基礎框架建置與版本追蹤。")
    
    # 查詢介面預留
    search_query = st.text_input("輸入 ETF 代號進行查詢 (開發中...):")
    
    if search_query:
        st.warning("功能模組建構中，請等待下一步指令。")

if __name__ == "__main__":
    main()