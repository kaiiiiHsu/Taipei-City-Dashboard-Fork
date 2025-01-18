import subprocess #傳遞參數腳本
import sys ##拿來讀傳遞的參數
import psycopg2 ##連資料庫
from datetime import datetime 
import os

# 測試print讀到的參數
def process_test(licensePlate):
    print(f"write successed: {licensePlate}")

# 配置資料庫連接信息
host = "localhost"        # Docker 容器地址或主機地址
port = "5434"                 # 端口號碼，例如 5432
database = "dashboard"        # 資料庫名稱
user = "postgres"             # 資料庫用戶名稱
password = "akaimio23693"     # 資料庫密碼
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

#####接收車牌辨識結果&照片編號#####

if __name__ == "__main__": #Python入口點，判斷檔案是否直接執行而非被當模組匯入
    if len(sys.argv) < 2:
        print("No ID provided!")
    else:
        licensePlate=sys.argv[1]
        photo_id=sys.argv[2]
    ###要再加車牌辨識錯誤碼###

#####寫入資料庫#####

try:
    # 創建游標
    cursor = connection.cursor()

    # 從 test_data 中查詢符合照片編號的記錄
    select_query = """
    SELECT 違規地點, 違規時間, "紀錄設備ID", 道路速限, 車輛時速
    FROM public.test_data
    WHERE 照片 = %s
    """
    cursor.execute(select_query, (photo_id,))
    record = cursor.fetchone()

    if record:
        #####經緯度轉換#####
        violation_location = record[0]  # 取出地點以獲取經緯度
        target_script = os.path.join("location", "location.py")  # 經緯度轉換程式的路徑
        result = subprocess.run(  # 執行目標程式
            ["python", target_script, violation_location],  # 傳遞目標程式及參數
            capture_output=True,  # 捕獲輸出
            text=True             # 將輸出作為文字
        )
        ##存下執行結果
        if result.returncode == 0:  # 確保程式執行成功
            if result.stdout=="無法獲取經緯度":
                print("經緯度轉換失敗")
            else:
                output = result.stdout.strip()  # 去除多餘的換行符
                longitude, latitude = output.split(",")  # 根據逗號分隔
                print(f"經度 = {longitude}, 緯度 = {latitude}")
        else:
            print(f"目標程式執行失敗，錯誤訊息：{result.stderr}")

        # 如果找到對應記錄，準備寫入 serial_data (燈桿提供的違規資料)
        違規地點, 違規時間, 紀錄設備ID, 道路速限, 車輛時速 = record
        車牌辨識最後時間 = datetime.now()

        # 插入數據到 serial_data
        insert_query = """
        INSERT INTO serial_data (
            違規照片, 違規地點, "紀錄設備ID", 道路速限, 車輛時速, 車牌辨識最後時間, 違規時間, 經度, 緯度, 車牌號碼
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (
            photo_id,
            違規地點,
            紀錄設備ID,
            道路速限,
            車輛時速,
            車牌辨識最後時間,
            違規時間,
            longitude,
            latitude,
            licensePlate
        ))

        # 提交更改
        connection.commit()
        print("數據寫入 serial_data 成功！")
    else:
        print(f"找不到照片編號為 {photo_id} 的記錄。")

except Exception as e:
    # 錯誤處理
    print("發生錯誤:", e)

finally:
    # 關閉游標和連接
    if 'cursor' in locals():
        cursor.close()
    if 'connection' in locals():
        connection.close()
        print("資料庫連接已關閉。")