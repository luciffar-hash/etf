import streamlit as st
import requests

# --- 版本控制 ---
VERSION = "0.2.1"

# --- 網頁配置 ---
st.set_page_config(
    page_title="路西法智庫：迦南金鑰",
    page_icon="🔑",
    layout="wide"
)

def get_wantgoo_etf_data(etf_id):
    """
    精確抓取玩股網即時市價與淨值數據
    """
    # 玩股網真實的個股/ETF 即時數據 API 節點
    url = f"https://www.wantgoo.com/api/equity/realtime/info?stockNo={etf_id}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": f"https://www.wantgoo.com/stock/{etf_id}"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            res_data = response.json()
            
            # 偵錯用：如果抓不到可以先看結構
            # st.write(res_data) 
            
            # 提取玩股網 JSON 欄位（真實欄位名稱依據其 API 結構調整）
            # 這裡加上安全防呆，若欄位不存在則給 0
            price = float(res_data.get("dealPrice", 0))    # 即時成交市價
            nav = float(res_data.get("nav", 0))            # 即時估計淨值
            
            # 如果主要節點沒抓到淨值，嘗試從另一個特定的 ETF 欄位抓取
            if nav == 0 and "etf" in res_data:
                nav = float(res_data["etf"].get("nav", 0))
                price = float(res_data["etf"].get("dealPrice", price))

            if price == 0 or nav == 0:
                return {"success": False, "msg": "未能成功解析市價或淨值欄位"}
                
            # 計算折溢價
            premium_value = price - nav
            premium_rate = (premium_value / nav)
            
            return {
                "success": True,
                "price": price,
                "nav": nav,
                "premium_value": premium_value,
                "premium_rate": premium_rate
            }
        else:
            return {"success": False, "msg": f"遠端伺服器回應錯誤碼: {response.status_code}"}
    except Exception as e:
        return {"success": False, "msg": f"網路連線或解析異常: {str(e)}"}

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
        with st.spinner("正在自數據深淵抽取真理..."):
            result = get_wantgoo_etf_data(etf_query)
            
            if result["success"]:
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
                    # 台股習慣：溢價（大於0）用紅、折價（小於0）用綠
                    color_style = "inverse" if p_value != 0 else "normal"
                    st.metric(label="折溢價金額", value=f"{p_value:+.2f}", delta_color=color_style)
                with col4:
                    st.metric(label="折溢價率", value=f"{p_rate:+.2%}", delta_color=color_style)
                
                # --- 風控診斷機制 ---
                if p_rate > 0.005:
                    st.error(f"🚨 高度溢價警告：目前溢價率達 {p_rate:.2%}！市價顯著高於實際淨值，請勿盲目追高。")
                elif p_rate < -0.005:
                    st.success(f"💡 折價狀態：目前折價率為 {p_rate:.2%}，市價相對淨值便宜。")
                else:
                    st.info("📊 折溢價處於正常合理區間（±0.5% 內）。")
            else:
                st.error(f"數據加載失敗：{result['msg']}")
                st.info("💡 提示：若持續失敗，可能是該代號無即時淨值更新，或玩股網 API 欄位微調。")

if __name__ == "__main__":
    main()
