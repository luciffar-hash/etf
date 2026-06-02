import streamlit as st
import requests
import pandas as pd

# --- 版本控制 ---
VERSION = "0.2.0"

# --- 網頁配置 ---
st.set_page_config(
    page_title="路西法智庫：迦南金鑰",
    page_icon="🔑",
    layout="wide"
)

# --- 核心邏輯：抓取即時淨值與市價 ---
def get_etf_data(etf_id):
    """
    透過玩股網 API 獲取即時市價與估計淨值
    """
    url = f"https://www.wantgoo.com/invest-api/etf/nav?symbol={etf_id}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            # 玩股網 API 回傳格式通常包含定價與淨值
            # 欄位說明：price(市價), nav(淨值), premiumRate(折溢價率)
            return {
                "success": True,
                "price": float(data.get("price", 0)),
                "nav": float(data.get("nav", 0)),
                "premium_rate": float(data.get("premiumRate", 0)),
                "premium_value": float(data.get("premiumPrice", 0))
            }
        else:
            return {"success": False, "msg": f"API 錯誤代碼: {response.status_code}"}
    except Exception as e:
        return {"success": False, "msg": f"連線異常: {str(e)}"}


def main():
    # --- 頁面標題與版號 ---
    st.title("🔑 路西法智庫：迦南金鑰")
    st.subheader("Luciffar AI: Canaan Key — Fully Automated ETF Insights")
    
    # 側邊欄
    st.sidebar.markdown(f"### 系統版本: {VERSION}")
    st.sidebar.info("路西法智庫，洞悉市場真理。")

    st.markdown("---")
    
    # --- 查詢介面 ---
    etf_query = st.text_input("輸入 ETF 代號:", value="0050").strip()
    
    if etf_query:
        with st.spinner("正在抽取市場真理數據..."):
            result = get_etf_data(etf_query)
            
            if result["success"] and result["nav"] > 0:
                price = result["price"]
                nav = result["nav"]
                p_value = result["premium_value"]
                p_rate = result["premium_rate"]
                
                # --- 數據排版展示 ---
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric(label="即時市價", value=f"{price:.2f}")
                with col2:
                    st.metric(label="最新淨值", value=f"{nav:.2f}")
                with col3:
                    # 色彩配置：溢價用紅、折價用綠（符合台股習慣）
                    color_style = "normal" if p_value == 0 else "inverse"
                    st.metric(label="折溢價金額", value=f"{p_value:+.2f}", delta_color=color_style)
                with col4:
                    st.metric(label="折溢價率", value=f"{p_rate:+.2%}", delta_color=color_style)
                
                # --- 智庫防呆警告機制 ---
                # 原型市值型 ETF 超過 0.5% 就屬於高溢價
                if p_rate > 0.005:
                    st.error(f"⚠️ 高度溢價警告：目前溢價率高達 {p_rate:.2%}！市價遠高於實際價值，請理性評估，避免盲目追高。")
                elif p_rate < -0.005:
                    st.success(f"💡 折價狀態：目前折價率為 {p_rate:.2%}，市價低於實際價值。")
                else:
                    st.info("📊 折溢價處於正常合理區間（±0.5% 內）。")
                    
            else:
                st.error(f"無法取得該 ETF 數據。錯誤原因：{result.get('msg', '查無此代號或資料未更新')}")

if __name__ == "__main__":
    main()
