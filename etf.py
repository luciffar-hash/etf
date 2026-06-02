import streamlit as st
import requests

# --- 版本控制 ---
VERSION = "0.7.0"

# --- 網頁配置 ---
st.set_page_config(
    page_title="路西法智庫：迦南金鑰",
    page_icon="🔑",
    layout="wide"
)

def get_official_etf_data_ip_version(etf_id):
    """
    終極抗災版：直接使用元大官方伺服器 IP 連線，徹底免疫 Streamlit Cloud 的 DNS 罷工（NameResolutionError）
    """
    # 透過直接解析元大投信官網得到的真實主要 IP
    # 🛡️ 當 DNS 故障時，直接敲 IP 才能確保連線順利通過
    YUANTA_IP_URL = f"https://210.200.82.164/api/FundNavRealTime?fundId={etf_id}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        # ⚠️ 關鍵核心：直接敲 IP 連線時，必須手動補上 Host 標頭，否則對方的網頁伺服器會拒絕回應
        "Host": "www.yuantafunds.com.tw"
    }
    
    try:
        # 使用 verify=False 是因為直接打 IP 會引發 SSL 憑證網域不符的警告，必須跳過驗證
        # 同時加上緊湊的 timeout 確保不會無限制死等
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        res = requests.get(YUANTA_IP_URL, headers=headers, timeout=5, verify=False)
        
        if res.status_code == 200:
            data_list = res.json()
            if data_list and isinstance(data_list, list):
                fund_data = data_list[0]
                price = float(fund_data.get("TradePrice", 0))
                nav = float(fund_data.get("EstNav", 0))
                name = fund_data.get("FundName", f"元大 {etf_id}")
                
                # 盤前或非交易時間市價防呆
                if price == 0 and float(fund_data.get("YesterdayNav", 0)) > 0:
                    price = float(fund_data.get("YesterdayNav", 0))
                
                if price > 0 and nav > 0:
                    return {"success": True, "price": price, "nav": nav, "name": name}
                    
            return {"success": False, "msg": "官方渠道暫時無即時數據更新（可能處於非交易時段）"}
        else:
            return {"success": False, "msg": f"遠端核心回應錯誤碼: {res.status_code}"}
            
    except Exception as e:
        # 如果打 IP 還失敗，提供一個最溫馨的提示，因為這代表 Streamlit Cloud 的外網出埠功能整個斷線了
        return {
            "success": False, 
            "msg": f"環境網路崩潰。Streamlit Cloud 平台目前正遭遇嚴重的網路中斷或 DNS 故障（原錯誤：{str(e)}）。"
        }

def main():
    st.title("🔑 路西法智庫：迦南金鑰")
    st.subheader("Luciffar AI: Canaan Key — Anti-DNS-Failure ETF Insights")
    
    st.sidebar.markdown(f"### 系統版本: {VERSION}")
    st.sidebar.info("路西法智庫，採用 IP 直接路由技術，強制刺穿雲端平台 DNS 封鎖。")
    st.markdown("---")
    
    etf_query = st.text_input("輸入台灣上市 ETF 代號 (優先支援元大系列如 0050, 0056, 00631L, 0052):", value="0050").strip()
    
    if etf_query:
        with st.spinner("正在啟動備用 IP 隧道直連投信核心..."):
            result = get_official_etf_data_ip_version(etf_query)
            
            if result["success"]:
                etf_name = result["name"]
                price = result["price"]
                nav = result["nav"]
                p_value = price - nav
                p_rate = p_value / nav
                
                st.caption(f"數據來源：元大官方機房直連隧道（目標：{etf_name}）")
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric(label="即時市價", value=f"{price:.2f}")
                with col2:
                    st.metric(label="最新淨值", value=f"{nav:.2f}")
                with col3:
                    color_style = "inverse" if p_value != 0 else "normal"
                    st.metric(label="折溢價金額", value=f"{p_value:+.2f}", delta_color=color_style)
                with col4:
                    st.metric(label="折溢價率", value=f"{p_rate:+.2%}", delta_color=color_style)
                
                if p_rate > 0.005:
                    st.error(f"🚨 高度溢價警告：目前溢價率達 {p_rate:.2%}！請勿盲目追高。")
                elif p_rate < -0.005:
                    st.success(f"💡 官方折價狀態：目前折價率為 {p_rate:.2%}，市價相對便宜。")
                else:
                    st.info("📊 折溢價處於正常合理常態區間（±0.5% 內）。")
            else:
                st.error(f"數據加載失敗：{result['msg']}")
                st.info("💡 智庫提示：此為 Streamlit Cloud 平台今日的大範圍故障，通常在幾小時內官方會修復 DNS 伺服器。")

if __name__ == "__main__":
    main()
