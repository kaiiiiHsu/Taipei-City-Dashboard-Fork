from dotenv import load_dotenv
import requests
import os

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
    # 測試地址
    address = "台北101"
    coordinates = get_lat_lng(address)
    if coordinates:
        print(f"地址: {address}")
        print(f"經緯度: 緯度 = {coordinates[0]}, 經度 = {coordinates[1]}")
    else:
        print("無法獲取經緯度")
