import streamlit as st
import requests
import time

# --- 版本控制 ---
VERSION = "0.4.0"

# --- 網頁配置 ---
st.set_page_config(
    page_title="路西法智庫：迦南金鑰",
    page_icon="🔑",
    layout="wide"
)

def get_twse_etf_data(etf_id):
    """
    直接對接臺灣證券交易所 (TWSE) 官方 API 獲取最權威的即時市價與估計淨值
    """
    # 1. 證交所官方 ETF 即時基本資料與估計淨值 API 節點
    nav_url = "https://mis.twse.com.tw/stock/api/getPrewEtfNav.jsp"
    
    # 2. 證交所官方個股即時盤口明細 API 節點 (用來精準比對市價)
    # 台股上市股票代號格式需為: tse_代號.tw
    stock_url = f"https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=tse_{etf_id}.tw"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        # --- 第一步：向證交所索取全市場 ETF 即時淨值清單 ---
        nav_response = requests.get(nav_url, headers=headers, timeout=5)
        if nav_response.status_code != 200:
            return {"success": False, "msg": f"證交所淨值伺服器回應錯誤: {nav_response.status_code}"}
        
        nav_data = nav_response.json()
        etf_list = nav_data.get("a1", []) # 證交所規定的 ETF 資料陣列 Key 為 'a1'
        
        # 在清單中尋找匹配目標代號的 ETF
        target_etf = None
        for etf in etf_list:
            # 證交所欄位：'a' 通常代表 ETF 代號
            if etf.get("a", "").strip() == etf_id:
                target_etf = etf
                break
                
        if not target_etf:
            return {"success": False, "msg": f"證交所即時清單中查無此上市 ETF 代號 ({etf_id})"}
        
        # 解析官方即時估計淨值
        # 欄位說明：'b' 代表今日最新估計淨值 (Estimated NAV)
        try:
            nav = float(target_etf.get("b", 0))
        except ValueError:
            return {"success": False, "msg": "證交所目前回傳之淨值格式異常或正處於盤前初始化"}

        # --- 第二步：同步向證交所索取該個股的精準即時交易市價 ---
        stock_response = requests.get(stock_url, headers=headers, timeout=5)
        price = 0.0
        
        if stock_response.status_code == 200:
            stock_data = stock_response.json()
            info_list = stock_data.get("msgArray", [])
            
            if info_list:
                stock_info = info_list[0]
                # 證交所盤口欄位說明：
                # 'z': 當盤成交價 (最新市價)
                # 'y': 昨收價 (若盤前還沒有成交價，以此替代防呆)
                # 'a': 最佳五檔買進價清單
                # 'b': 最佳五檔賣出價清單
                z_val = stock_info.get("z", "-")
                if z_val != "-":
                    price = float(z_val)
                else:
                    # 若當前剛好暫停交易或處於盤前未有成交價，改抓昨收價或最佳買價防呆
                    price = float(stock_info.get("y", 0))

        # 如果從個股節點沒抓到市價，則啟動備援：直接使用 ETF 淨值節點自帶的市價欄位（欄位 'c'）
        if price == 0:
            try:
                price = float(target_etf.get("c", 0))
            except ValueError:
                price = 0.0

        if price == 0 or nav == 0:
            return {"success": False, "msg": f"證交所目前未提供該 ETF 之有效即時報價（市價:{price} / 淨值:{nav}）"}

        # --- 第三步：嚴謹進行數學計算 ---
        premium_value = price - nav
        premium_rate = premium_value / nav
        
        return {
            "success": True,
            "name": target_etf.get("e", f"ETF {etf_id}"), # 'e' 欄位為 ETF 官方簡稱
            "price": price,
            "nav": nav,
            "premium_value": premium_value,
            "premium_rate": premium_rate
        }
        
    except Exception as e:
        return {"success": False, "msg": f"對接證交所系統發生異常連線中斷: {str(e)}"}

def main():
    # --- 頁面標題與版號 ---
    st.title("🔑 路西法智庫：迦南金鑰")
    st.subheader("Luciffar AI: Canaan Key — TWSE Official Real-Time ETF Insights")
    
    # 側邊欄
    st.sidebar.markdown(f"### 系統版本: {VERSION}")
    st.sidebar.info("路西法智庫，直接對接臺灣證券交易所官方數據源，洞悉市場不變之真理。")

    st.markdown("---")
    
    # --- 查詢介面 ---
    etf_query = st.text_input("輸入台灣上市 ETF 代號 (支援全市場上市 ETF，如 0050, 0056, 006208, 00878):", value="0050").strip()
    
    if etf_query:
        with st.spinner("正在直連臺灣證券交易所核心資料庫..."):
            result = get_twse_etf_data(etf_query)
            
            if result["success"]:
                etf_name = result["name"]
                price = result["price"]
                nav = result["nav"]
                p_value = result["premium_value"]
                p_rate = result["premium_rate"]
                
                # 顯示 ETF 官方名稱
                st.caption(f"當前查詢目標：**{etf_name}**")
                
                # --- 數據排版展示 ---
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric(label="官方即時市價", value=f"{price:.2f}")
                with col2:
                    st.metric(label="官方最新估計淨值", value=f"{nav:.2f}")
                with col3:
                    color_style = "inverse" if p_value != 0 else "normal"
                    st.metric(label="折溢價金額", value=f"{p_value:+.2f}", delta_color=color_style)
                with col4:
                    st.metric(label="折溢價率", value=f"{p_rate:+.2%}", delta_color=color_style)
                
                # --- 風控診斷機制 ---
                if p_rate > 0.005:
                    st.error(f"🚨 權威溢價警告：目前溢價率達 {p_rate:.2%}！市價已顯著高於官方實際淨值，請勿盲目追高。")
                elif p_rate < -0.005:
                    st.success(f"💡 官方折價狀態：目前折價率為 {p_rate:.2%}，市價相對便宜。")
                else:
                    st.info("📊 折溢價處於官方認定之正常合理常態區間（±0.5% 內）。")
            else:
                st.error(f"數據加載失敗：{result['msg']}")
                st.info("💡 提示：請確保輸入的是在「臺灣證券交易所」上市的原型或槓桿型 ETF。")

if __name__ == "__main__":
    main()
