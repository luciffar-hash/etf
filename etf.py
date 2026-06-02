import streamlit as st
import requests

# --- 版本控制 ---
VERSION = "0.3.0"

# --- 網頁配置 ---
st.set_page_config(
    page_title="路西法智庫：迦南金鑰",
    page_icon="🔑",
    layout="wide"
)

def get_yuanta_etf_data(etf_id):
    """
    直接從元大投信官方 API 獲取即時估計淨值與市價
    """
    # 元大官方即時估計淨值與市價 API
    url = f"https://www.yuantafunds.com.tw/api/FundNavRealTime?fundId={etf_id}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            data_list = response.json()
            
            # 元大 API 回傳通常是一個陣列，若查無資料會是空陣列
            if not data_list:
                return {"success": False, "msg": f"元大官網查無此代號 ({etf_id})，或該 ETF 非元大發行"}
            
            # 取得第一筆資料
            fund_data = data_list[0]
            
            # 解析元大官方欄位
            # 欄位說明：TradePrice(即時市價), EstNav(估計淨值), PremiumRate(折溢價率)
            price = float(fund_data.get("TradePrice", 0))
            nav = float(fund_data.get("EstNav", 0))
            
            # 若盤前或非交易時間官方市價回傳 0，則防呆處理
            if price == 0 or nav == 0:
                return {"success": False, "msg": f"官方目前未提供即時報價（市價:{price} / 淨值:{nav}）"}
            
            # 計算折溢價
            premium_value = price - nav
            premium_rate = premium_value / nav
            
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
    etf_query = st.text_input("輸入 ETF 代號 (支援元大發行之 ETF，如 0050, 0056, 0052):", value="0050").strip()
    
    if etf_query:
        with st.spinner("正在自官方渠道抽取真理數據..."):
            result = get_yuanta_etf_data(etf_query)
            
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
                st.info("💡 提示：本版本直接對接元大投信 API，請確保輸入的是元大發行的 ETF 代號。")

if __name__ == "__main__":
    main()
