def get_wantgoo_etf_data(etf_id):
    """
    精確抓取玩股網即時市價與淨值數據（強化防 403 阻擋版本）
    """
    url = f"https://www.wantgoo.com/api/equity/realtime/info?stockNo={etf_id}"
    
    # 建立一個與瀏覽器完全一致的 Session，自動處理 Cookie
    session = requests.Session()
    
    # 擬真瀏覽器標頭，加入完整的驗證資訊
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Origin": "https://www.wantgoo.com",
        "Referer": f"https://www.wantgoo.com/stock/{etf_id}",
        "Sec-Ch-Ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "X-Requested-With": "XMLHttpRequest"
    }
    
    try:
        # 先上一動：模擬真人先訪問一次首頁，讓 Session 拿到並種下基礎 Cookie
        session.get(f"https://www.wantgoo.com/stock/{etf_id}", headers={"User-Agent": headers["User-Agent"]}, timeout=5)
        
        # 第二動：帶上剛才拿到的 Cookie 與完整標頭，正式請求 API
        response = session.get(url, headers=headers, timeout=5)
        
        if response.status_code == 200:
            res_data = response.json()
            
            # 提取玩股網 JSON 欄位
            price = float(res_data.get("dealPrice", 0))    # 即時成交市價
            nav = float(res_data.get("nav", 0))            # 即時估計淨值
            
            if nav == 0 and "etf" in res_data:
                nav = float(res_data["etf"].get("nav", 0))
                price = float(res_data["etf"].get("dealPrice", price))

            if price == 0 or nav == 0:
                return {"success": False, "msg": f"未能成功解析市價或淨值欄位（市價:{price}/淨值:{nav}）"}
                
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
            return {"success": False, "msg": f"遠端伺服器回應錯誤碼: {response.status_code} (伺服器拒絕雲端主機連線)"}
    except Exception as e:
        return {"success": False, "msg": f"網路連線或解析異常: {str(e)}"}
