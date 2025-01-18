import subprocess #傳遞參數腳本
import os

# 指定目標程式的路徑
target_script = os.path.join("location", "location.py")

# 傳遞參數給目標程式
violation_location = "新北市板橋區文聖國小"

# 執行目標程式
result = subprocess.run(
    ["python", target_script, violation_location],  # 傳遞目標程式及參數
    capture_output=True,  # 捕獲輸出
    text=True             # 將輸出作為文字
)

##印出執行結果
if result.returncode == 0:  # 確保程式執行成功
    if result.stdout=="無法獲取經緯度":
        print("經緯度轉換失敗")
    else:
        output = result.stdout.strip()  # 去除多餘的換行符
        longitude, latitude = output.split(",")  # 根據逗號分隔
        print(f"經度 = {longitude}, 緯度 = {latitude}")
else:
    print(f"目標程式執行失敗，錯誤訊息：{result.stderr}")