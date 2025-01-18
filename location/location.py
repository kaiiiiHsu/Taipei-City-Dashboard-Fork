from dotenv import load_dotenv
import requests
import os
import subprocess #傳遞參數腳本
import sys ##拿來讀傳遞的參數

load_dotenv()
api_key = os.getenv('API_KEY')
# 使用 Google Geocoding API 將地址轉換為經緯度
def get_lat_lng(address):    
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": address, "key": api_key}    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data['status'] == "OK":
            location = data['results'][0]['geometry']['location']
            return location['lat'], location['lng']
        else:
            print("Geocoding failed:", data['status'])
            return None
    except requests.exceptions.RequestException as e:
        print("Request failed:", e)
        return None

# 主程式
if __name__ == "__main__":
    if len(sys.argv) < 2:
        param = "default"
    else:
        address=sys.argv[1]
    # 測試地址
    coordinates = get_lat_lng(address)
    if coordinates:
        #print(f"地址: {address}")
        print(f"{coordinates[0]},{coordinates[1]}") # 經度, 緯度
    else:
        print("無法獲取經緯度")
