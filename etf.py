import streamlit as st
import requests

# --- 版本控制 ---
VERSION = "0.5.0"

# --- 網頁配置 ---
st.set_page_config(
    page_title="路西法智庫：迦南金鑰",
    page_icon="🔑",
    layout="wide"
)

def get_twse_open_data_etf(etf_id):
    """
    直連臺灣證券交易所 (TWSE) 開放資料核心節點
    一次性精準獲取全市場 ETF 當前最新市價與官方淨值，完美解決 403 與 404 痛點
    """
    # 證交所官方維護之全市場上市 ETF 盤中即時折溢價與淨值開放資料節點
    url = "https://openapi.twse.com.tw/v1/etf/etfNav"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "accept": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=6)
        
        if response.status_code == 200:
            etf_list = response.json()
            
            # 在資料庫中尋找目標 ETF 代號
            target_data = None
            for item in etf_list:
                # 證交所 Open Data 欄位：'Code' 代表 ETF 代號
                if item.get("Code", "").strip() == etf_id:
                    target_data = item
                    break
            
            if not target_data:
                return {"success": False, "msg": f"證交所官方當前名冊中，查無此上市 ETF 代號 ({etf_id})"}
            
            # 解析證交所權威欄位資料
            # 欄位說明：
            # 'Name': ETF 官方名稱
            # 'TradePrice': 當前最新市場成交價 (市價)
            # 'Nav': 官方計算之最新估計淨值 (NAV)
            try:
                price = float(target_data.get("TradePrice", 0))
                nav = float(target_data.get("Nav", 0))
                etf_name = target_data.get("Name", f"ETF {etf_id}")
            except (ValueError, TypeError):
                return {"success": False, "msg": "證交所回傳之數據格式異常，可能正處於非交易時段之系統維護"}
                
            if price == 0 or nav == 0:
                return {"success": False, "msg": f"官方目前數據未初始化或尚未開盤（市價:{price} / 淨值:{nav}）"}
                
            # 計算最精準的折溢價
            premium_value = price - nav
            premium_rate = premium_value / nav
            
            return {
                "success": True,
                "name": etf_name,
                "price": price,
                "nav": nav,
                "premium_value": premium_value,
                "premium_rate": premium_rate
            }
        else:
            return {"success": False, "msg": f"臺灣證券交易所伺服器拒絕連線，錯誤碼: {response.status_code}"}
            
    except Exception as e:
        return {"success": False, "msg": f"直連國家證券核心資料庫發生連線異常: {str(e)}"}

def main():
    # --- 頁面標題與版號 ---
    st.title("🔑 路西法智庫：迦南金鑰")
    st.subheader("Luciffar AI: Canaan Key — TWSE OpenData Real-Time ETF Insights")
    
    # 側邊欄
    st.sidebar.markdown(f"### 系統版本: {VERSION}")
    st.sidebar.info("路西法智庫，直連臺灣證券交易所 Open Data 權威資料庫，洞悉市場不變之真理。")

    st.markdown("---")
    
    # --- 查詢介面 ---
    etf_query = st.text_input("輸入台灣上市 ETF 代號 (支援全台灣上市股票型、市值型、槓桿型 ETF):", value="0050").strip()
    
    if etf_query:
        with st.spinner("正在直連臺灣證券交易所核心資料庫..."):
            result = get_twse_open_data_etf(etf_query)
            
            if result["success"]:
                etf_name = result["name"]
                price = result["price"]
                nav = result["nav"]
                p_value = result["premium_value"]
                p_rate = result["premium_rate"]
                
                # 顯示官方正規劃的商品簡稱
                st.caption(f"當前查詢目標：**{etf_name}**")
                
                # --- 數據排版展示 ---
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric(label="官方即時市價", value=f"{price:.2f}")
                with col2:
                    st.metric(label="官方權威淨值", value=f"{nav:.2f}")
                with col3:
                    # 台股習慣：溢價（市價大於淨值）用紅、折價用綠
                    color_style = "inverse" if p_value != 0 else "normal"
                    st.metric(label="折溢價金額", value=f"{p_value:+.2f}", delta_color=color_style)
                with col4:
                    st.metric(label="折溢價率", value=f"{p_rate:+.2%}", delta_color=color_style)
                
                # --- 智庫風控診斷機制 ---
                if p_rate > 0.005:
                    st.error(f"🚨 權威溢價警告：目前溢價率達 {p_rate:.2%}！市價已顯著高於官方實際價值，請勿盲目追高。")
                elif p_rate < -0.005:
                    st.success(f"💡 官方折價狀態：目前折價率為 {p_rate:.2%}，市價相對實際淨值更便宜。")
                else:
                    st.info("📊 折溢價處於官方認定之正常合理常態區間（±0.5% 內）。")
            else:
                st.error(f"數據加載失敗：{result['msg']}")
                st.info("💡 提示：本版本直接調用證交所 OpenAPI。請確保輸入的代號（例如 0050, 0056, 006208）已在臺灣證券交易所正式掛牌上市。")

if __name__ == "__main__":
    main()
