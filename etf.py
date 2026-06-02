import streamlit as st
import requests

# --- 版本控制 ---
VERSION = "0.6.0"

# --- 網頁配置 ---
st.set_page_config(
    page_title="路西法智庫：迦南金鑰",
    page_icon="🔑",
    layout="wide"
)

def get_official_etf_data(etf_id):
    """
    直連元大/富邦投信官方即時 API 機制，繞過證交所頻繁維護與 IP 阻擋問題
    """
    # 宣告常見的富邦 ETF 代號清單，用來做自動分流
    fubon_list = ["006208", "00692", "0057", "00700", "00733"]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    # --- 路由 A：富邦投信官方管道 ---
    if etf_id in fubon_list:
        url = f"https://www.fubon.com/asset-management/api/fund/nav/real-time?fundCode={etf_id}"
        try:
            res = requests.get(url, headers=headers, timeout=5)
            if res.status_code == 200:
                data = res.json()
                # 富邦 API 結構解析
                price = float(data.get("tradePrice", 0))
                nav = float(data.get("estNav", 0))
                name = data.get("fundName", f"富邦 {etf_id}")
                
                if price > 0 and nav > 0:
                    return {"success": True, "price": price, "nav": nav, "name": name, "source": "富邦官方"}
        except:
            pass

    # --- 路由 B：元大投信官方管道 (預設主路由，包含 0050, 0056, 00631L 等) ---
    url = f"https://www.yuantafunds.com.tw/api/FundNavRealTime?fundId={etf_id}"
    try:
        res = requests.get(url, headers=headers, timeout=5)
        if res.status_code == 200:
            data_list = res.json()
            if data_list and isinstance(data_list, list):
                fund_data = data_list[0]
                price = float(fund_data.get("TradePrice", 0))
                nav = float(fund_data.get("EstNav", 0))
                name = fund_data.get("FundName", f"元大 {etf_id}")
                
                # 如果盤前市價為 0，改用昨收價防呆
                if price == 0 and float(fund_data.get("YesterdayNav", 0)) > 0:
                    price = float(fund_data.get("YesterdayNav", 0))
                
                if price > 0 and nav > 0:
                    return {"success": True, "price": price, "nav": nav, "name": name, "source": "元大官方"}
    except Exception as e:
        return {"success": False, "msg": f"投信伺服器連線異常: {str(e)}"}

    return {"success": False, "msg": f"目前官方管道查無此代號 ({etf_id})，或非元大/富邦發行之上市 ETF"}

def main():
    st.title("🔑 路西法智庫：迦南金鑰")
    st.subheader("Luciffar AI: Canaan Key — Fund Official Real-Time ETF Insights")
    
    st.sidebar.markdown(f"### 系統版本: {VERSION}")
    st.sidebar.info("路西法智庫，對接投信官方綠色通道，確保市場數據真理絕不中斷。")
    st.markdown("---")
    
    etf_query = st.text_input("輸入台灣上市 ETF 代號 (支援 0050, 0056, 006208, 0052 等):", value="0050").strip()
    
    if etf_query:
        with st.spinner("正在直連投信核心報價系統..."):
            result = get_official_etf_data(etf_query)
            
            if result["success"]:
                etf_name = result["name"]
                price = result["price"]
                nav = result["nav"]
                p_value = price - nav
                p_rate = p_value / nav
                
                st.caption(f"數據來源：官方認證 **{result['source']}** 渠道（目標：{etf_name}）")
                
                # --- 數據排版展示 ---
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric(label="官方即時市價", value=f"{price:.2f}")
                with col2:
                    st.metric(label="官方最新淨值", value=f"{nav:.2f}")
                with col3:
                    color_style = "inverse" if p_value != 0 else "normal"
                    st.metric(label="折溢價金額", value=f"{p_value:+.2f}", delta_color=color_style)
                with col4:
                    st.metric(label="折溢價率", value=f"{p_rate:+.2%}", delta_color=color_style)
                
                # --- 智庫風控診斷機制 ---
                if p_rate > 0.005:
                    st.error(f"🚨 高度溢價警告：目前溢價率達 {p_rate:.2%}！市價顯著高於實際價值，請理性評估。")
                elif p_rate < -0.005:
                    st.success(f"💡 官方折價狀態：目前折價率為 {p_rate:.2%}，市價相對划算。")
                else:
                    st.info("📊 折溢價處於正常合理常態區間（±0.5% 內）。")
            else:
                st.error(f"數據加載失敗：{result['msg']}")

if __name__ == "__main__":
    main()
