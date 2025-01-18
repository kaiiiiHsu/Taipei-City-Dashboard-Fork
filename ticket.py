import psycopg2  # 連接資料庫
from datetime import datetime  # 用於取得現在時間

# 配置資料庫連接信息
db_config = {
    "host": "localhost",
    "port": "5434",
    "database": "dashboard",
    "user": "postgres",
    "password": "password",
}

# 查詢SQL語句
query_serial_data = "SELECT * FROM public.serial_data;"
query_car_info = """
    SELECT 車籍回覆碼, 車主姓名, 車主地址 
    FROM public.car_info 
    WHERE 車牌號碼 = %s;
"""
update_serial_data = "UPDATE public.serial_data SET timestamp = %s WHERE 車牌號碼 = %s;"
update_car_info = "UPDATE public.car_info SET timestamp = %s WHERE 車牌號碼 = %s;"

try:
    # 建立資料庫連接
    connection = psycopg2.connect(**db_config)
    print("連接到資料庫成功")

    # 執行查詢並處理資料
    with connection.cursor() as cursor:
        # 查詢 serial_data 資料表
        cursor.execute(query_serial_data)
        serial_data_rows = cursor.fetchall()

        print("查詢結果：")
        for index, row in enumerate(serial_data_rows):
            # 假設車牌號碼在 serial_data 中的第 8 欄位
            plate_number = row[8]
            print(f"第 {index + 1} 筆資料 - 車牌號碼：{plate_number}")

            # 更新 serial_data 的 timestamp
            now = datetime.now()
            cursor.execute(update_serial_data, (now, plate_number))

            # 查詢 car_info 資料表是否有匹配的車牌號碼
            cursor.execute(query_car_info, (plate_number,))
            car_info_row = cursor.fetchone()

            # 判斷是否找到匹配的車牌號碼
            if car_info_row:
                car_reply_code, owner_name, owner_address = car_info_row
                print(f"車籍回覆碼：{car_reply_code}")
                print(f"車主姓名：{owner_name}")
                print(f"車主地址：{owner_address}")
                
                # 更新 car_info 的 timestamp
                cursor.execute(update_car_info, (now, plate_number))
            else:
                print("無此車牌")

        # 提交所有更改
        connection.commit()
        print("所有更新已提交")

except Exception as e:
    print(f"資料庫錯誤：{e}")

finally:
    # 關閉資料庫連接
    if connection:
        connection.close()
        print("資料庫連接已關閉。")
