import psycopg2
from datetime import datetime

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
        password=password  # 密码
    )
    cursor = connection.cursor()
    print("連接到資料庫成功")
except Exception as e:
    print(f"資料庫連接失敗：{e}")
    exit()

try:
    # 創建游標
    cursor = connection.cursor()

    # 要插入的數據
    data = {
        "舉發ID": 6,
        "違規照片": "photo_006.jpg",
        "違規地點": "台北市文山區木新路三段",
        "經度": 121.5595052,
        "緯度": 24.9814114,
        "紀錄設備ID": "DEV00561",
        "道路速限": 60,
        "車輛時速": 80,
        "車牌號碼": "ABC-1666",
        "車牌辨識錯誤碼": "ERR_001",
        "車牌辨識最後時間": datetime(2024, 12, 31, 14, 0, 0),  # 年/月/日/時/分/秒
        "違規時間": datetime(2024, 12, 31, 13, 55, 0)          # 年/月/日/時/分/秒
    }

    # 插入資料庫的SQL語句
    insert_query = """
    INSERT INTO public.serial_data (
        "舉發ID", 違規照片, 違規地點, 經度, 緯度,
        "紀錄設備ID", 道路速限, 車輛時速, 車牌號碼, 車牌辨識錯誤碼,
        車牌辨識最後時間, 違規時間
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    # 執行插入
    cursor.execute(insert_query, (
        data["舉發ID"],
        data["違規照片"],
        data["違規地點"],
        data["經度"],
        data["緯度"],
        data["紀錄設備ID"],
        data["道路速限"],
        data["車輛時速"],
        data["車牌號碼"],
        data["車牌辨識錯誤碼"],
        data["車牌辨識最後時間"],
        data["違規時間"]
    ))

    # 提交更改
    connection.commit()
    print("資料插入成功成功！")

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