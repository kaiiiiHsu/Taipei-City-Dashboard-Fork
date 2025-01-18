import subprocess
import os

photo_name = "A03" # 取出照片檔名
target_script = os.path.join("..","YOLOv8-License-Plate-Insights-main", "inference.py")  # 經緯度轉換程式的路徑
result = subprocess.run(
    ["python", target_script, photo_name],
    capture_output=True,
    text=True,
    encoding='utf-8'
)

if result.returncode == 0:
    if result.stdout.strip() == "無法獲取車牌辨識結果":
        print("車牌辨識失敗")
        license_plate, plate_error = None, None
    else:
        license_plate, plate_error = result.stdout.strip().split(",")
        print(f"Captured License Plate: {license_plate}") # <-車牌辨識結果！#####
        print(f"Plate Error: {plate_error}") # <-錯誤代碼！#####
else:
    print(f"目標程式執行失敗，錯誤訊息：{result.stderr}")
    license_plate = None

'''command = ["python", "inference.py"]  # 使用適當的檔案名稱
result = subprocess.run(command, capture_output=True, text=True)

# 抓取並清理結果
license_plate = result.stdout.strip()
print(f"Captured License Plate: {license_plate}") #<-車牌辨識結果！#####'''