import subprocess #傳遞參數腳本
import psycopg2 ##連資料庫
import json
from datetime import datetime 
import os

# 配置資料庫連接信息
host = "localhost"        # Docker 容器地址或主機地址
port = "5434"                 # 端口號碼，例如 5432
database = "dashboard"        # 資料庫名稱
user = "postgres"             # 資料庫用戶名稱
password = "password"     # 資料庫密碼
options="-c client_encoding=UTF8"

# 連接到 PostgreSQL 資料庫
try:
    connection = psycopg2.connect(
        host=host,         # PostgreSQL 主機
        port=port,              # 默認端口是 5432
        database=database,   # 資料庫名稱
        user=user,          # 用戶名
        password=password  # 密碼
    )
    cursor = connection.cursor()
    print("連接到資料庫成功")
except Exception as e:
    print(f"資料庫連接失敗：{e}")
    exit()

#####寫入資料庫#####
try:
    # 創建游標
    cursor = connection.cursor()

    # 查詢SQL語句
    query = "SELECT * FROM public.test_data;"
    cursor.execute(query)

    # 使用 fetchall 提取所有結果
    rows = cursor.fetchall()

    # 打開現有的 GeoJSON 文件
    geojson_file_path = "Taipei-City-Dashboard-FE\\public\\mapData\\serial_data.geojson"
    try:
        with open(geojson_file_path, "r", encoding="utf-8") as geojson_file:
            geojson_data = json.load(geojson_file)
    except FileNotFoundError:
        # 如果文件不存在，初始化一个新的 GeoJSON
        geojson_data = {
            "type": "FeatureCollection",
            "features": []
        }
    # 開始讀取測試資料庫
    if not rows:
        print("沒有找到任何資料！")
    else:
        print("開始讀取資料：")
        for counter, row in enumerate(rows, start=1):
            print(f"第 {counter} 筆資料：\n", row)

            ##### 經緯度轉換 #####
            violation_location = row[1]  # 取出地點
            target_script = os.path.join("location", "location.py")  # 經緯度轉換程式的路徑
            result = subprocess.run(
                ["python", target_script, violation_location],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                if result.stdout.strip() == "無法獲取經緯度":
                    print("經緯度轉換失敗")
                    longitude, latitude = None, None
                else:
                    longitude, latitude = result.stdout.strip().split(",")
                    print(f"經度 = {longitude}, 緯度 = {latitude}")
            else:
                print(f"目標程式執行失敗，錯誤訊息：{result.stderr}")
                longitude, latitude = None, None

            ##### 車牌相關 #####
            
            photo_name = row[0]  # 取出照片檔名
            target_script = os.path.join("..","YOLOv8-License-Plate-Insights-main", "inference.py")  # 經緯度轉換程式的路徑
            result = subprocess.run(
                ["python", target_script, photo_name],
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            #####接收車牌辨識結果/錯誤訊息：多車牌，無法辨識#####
            if result.returncode == 0:
                if result.stdout.strip() == "無法獲取車牌辨識結果":
                    print("車牌辨識失敗")
                    license_plate, plate_error = None, None
                    status = "待處理"
                else:
                    license_plate, plate_error = result.stdout.strip().split(",")
                    print(f"Captured License Plate: {license_plate}") # <-車牌辨識結果！#####
                    print(f"Plate Error: {plate_error}") # <-錯誤代碼！#####
                    if(plate_error!="NULL"):
                        status = "待處理"
                    else:
                        status = "已處理"
            else:
                print(f"目標程式執行失敗，錯誤訊息：{result.stderr}")
                license_plate = None

            ##### 寫入燈桿提供的違規資料 serial_data #####
            photo_id,location, timestamp, 紀錄設備ID, 道路速限, 車輛時速 = row
            車牌辨識最後時間 = datetime.now()

            # 插入數據到 serial_data
            insert_query = """
            INSERT INTO serial_data (
                "image", "location", "紀錄設備ID", 道路速限, 車輛時速, 車牌辨識最後時間, "timestamp", 經度, 緯度, 車牌號碼,車牌辨識錯誤碼,"status"
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING "id";
            """
            with connection.cursor() as insert_cursor: # 創建臨時游標進行插入，避免與查詢操作混用游標
                insert_cursor.execute(insert_query, (
                    photo_id,
                    location,
                    紀錄設備ID,
                    道路速限,
                    車輛時速,
                    車牌辨識最後時間,
                    timestamp,
                    longitude,
                    latitude,
                    license_plate,
                    plate_error,
                    #location[:3], # 前三字為行政區
                    status
                ))
            # generated_id = cursor.fetchone()[0]
                result = insert_cursor.fetchone()
                if result is None:
                    print("未找到任何返回结果，請檢察查詢條件或資料表")
                else:
                    generated_id = result[0]

            # 將記錄追加到 GeoJSON 中
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [float(latitude), float(longitude)]
                },
                "properties": {
                    "id": generated_id,
                    "image":photo_id,
                    "location": location,
                    "紀錄設備ID": 紀錄設備ID,
                    "道路速限":float(道路速限),
                    "車輛時速":float(車輛時速),
                    "車牌號碼":license_plate,
                    "車牌辨識錯誤碼":plate_error,
                    "車牌辨識最後時間":(datetime.now()).strftime("%Y-%m-%d %H:%M:%S"),
                    "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    "district":location[3:6],
                    "status":status
                },

            }
            geojson_data["features"].append(feature)

            # 提交更改
            connection.commit()
            print("數據寫入 serial_data 成功！")
            
            # 更新 GeoJSON 文件
            with open(geojson_file_path, "w", encoding="utf-8") as geojson_file:
                json.dump(geojson_data, geojson_file, ensure_ascii=False, indent=4)

            print("GeoJSON 文件已更新")

            
            
except Exception as e:
    print(f"資料庫錯誤：{e}")
finally:
    # 關閉連線和游標
    if cursor:
        cursor.close()
    if connection:
        connection.close()
        print("資料庫連接已關閉。")
