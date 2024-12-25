import PIL
from PIL import Image
import glob
import shutil, os
from time import sleep
import cv2
import numpy as np
import sys
import pyocr
import pyocr.builders
import re

# 手動指定 Tesseract 的安裝路徑
os.environ['TESSDATA_PREFIX'] = r".car\\Tesseract-OCR"
os.environ['PATH'] += os.pathsep + r".car\\Tesseract-OCR"


def emptydir(dirname):         #清空資料夾
    if os.path.isdir(dirname): #資料夾存在就刪除
        shutil.rmtree(dirname)
        sleep(2)       #需延遲,否則會出錯
    os.mkdir(dirname)  #建立資料夾

def dirResize(src, dst):
    myfiles = glob.glob(src + '/*.JPG') #讀取資料夾全部jpg檔案
    emptydir(dst)
    print(' 資料夾：' + src)
    print('開始轉換圖形尺寸！')
    for f in myfiles:
        fname = f.split("\\")[-1]
        img = Image.open(f)
        img_new = img.resize((300, 225), PIL.Image.LANCZOS)  #尺寸300x225
        img_new.save(dst + '/' + fname)
    print('轉換圖形尺寸完成！\n')
files = glob.glob("predictPlate/*.jpg")
dirResize('predictPlate', 'predictPlate_resized')

for file in files:
    print('圖片檔案：' + file)
    img = cv2.imread(file)
    detector = cv2.CascadeClassifier('haar_carplate.xml')
    signs = detector.detectMultiScale(img, minSize=(76, 20), scaleFactor=1.1, minNeighbors=4)
    if len(signs) > 0 :
        for (x, y, w, h) in signs:          
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)  
            print(signs)
    else:
        print('沒有偵測到車牌！')
    
    cv2.imshow('Frame', img)
    key = cv2.waitKey(0)
    cv2.destroyAllWindows()
    if key == 113 or key==81:  #按q鍵結束
        break
#####################################################

print('開始擷取車牌！')
print('無法擷取車牌的圖片：')
dstdir = 'cropPlate'
emptydir(dstdir)
myfiles = glob.glob("predictPlate_resized\*.JPG")
for imgname in myfiles:
    filename = (imgname.split('\\'))[-1]  #取得檔案名稱
    img = cv2.imread(imgname)  #讀入圖形
    detector = cv2.CascadeClassifier('haar_carplate.xml')
    signs = detector.detectMultiScale(img, scaleFactor=1.1, minNeighbors=4, minSize=(20, 20))  #框出車牌
    #擷取車牌
    if len(signs) > 0 :
        for (x, y, w, h) in signs:          
            image1 = Image.open(imgname)
            image2 = image1.crop((x, y, x+w, y+h))  #擷取車牌圖形
            image3 = image2.resize((140, 40), Image.LANCZOS) #轉換尺寸為140X40
            img_gray = np.array(image3.convert('L'))  #灰階
            _, img_thre = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY) #黑白
            cv2.imwrite(dstdir + '/'+ filename, img_thre) #存檔
    else:
        print(filename)

print('擷取車牌結束！')
#############################################################################################

# 設定圖片來源資料夾與處理後儲存資料夾
input_folder = ".\\car\\cropPlate\\"
output_folder = ".\\car\\processed\\"

# 確保輸出資料夾存在
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 取得所有 JPG 圖片的完整路徑
image_paths = glob.glob(os.path.join(input_folder, "*.jpg"))

def area(row, col):
    global nn, bg, lifearea
    if bg[row][col] != 255:
        return
    bg[row][col] = lifearea  # 記錄生命區的編號
    if col > 1:  # 左方
        if bg[row][col-1] == 255:
            nn += 1
            area(row, col-1)
    if col < w-1:  # 右方
        if bg[row][col+1] == 255:
            nn += 1
            area(row, col+1)
    if row > 1:  # 上方
        if bg[row-1][col] == 255:
            nn += 1
            area(row-1, col)
    if row < h-1:  # 下方
        if bg[row+1][col] == 255:
            nn += 1
            area(row+1, col)

# 遍歷每張圖片並處理
for image_path in image_paths:
    # 讀取圖片
    image = cv2.imread(image_path)
    if image is None:
        print(f"無法讀取圖片: {image_path}")
        continue

    print(f"處理圖片: {image_path}")
    image_name = os.path.basename(image_path)  # 取得檔案名稱
    output_path = os.path.join(output_folder, f"processed_{image_name}")  # 輸出路徑

    # 灰階處理
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)

    # 尋找輪廓
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    letter_image_regions = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        letter_image_regions.append((x, y, w, h))
    letter_image_regions = sorted(letter_image_regions, key=lambda x: x[0])  # 按 X 坐標排序

    # 檢查字元數量
    count = 0
    for box in letter_image_regions:
        x, y, w, h = box
        if x >= 2 and x <= 125 and w >= 5 and w <= 26 and h >= 20 and h < 40:
            count += 1
    wmax = 35 if count < 6 else 26

    # 篩選字元
    nChar = 0
    letterlist = []
    for box in letter_image_regions:
        x, y, w, h = box
        if x >= 2 and x <= 125 and w >= 5 and w <= wmax and h >= 20 and h < 40:
            nChar += 1
            letterlist.append((x, y, w, h))

    # 去除雜點
    for i in range(len(thresh)):
        for j in range(len(thresh[i])):
            if thresh[i][j] == 255:
                count = 0
                for k in range(-2, 3):
                    for l in range(-2, 3):
                        try:
                            if thresh[i + k][j + l] == 255:
                                count += 1
                        except IndexError:
                            pass
                if count <= 6:
                    thresh[i][j] = 0

    # 提取有效字元
    real_shape = []
    for i, box in enumerate(letterlist):
        x, y, w, h = box
        bg = thresh[y:y+h, x:x+w]
        if i == 0 or i == nChar - 1:
            lifearea = 0
            nn = 0
            life = []
            for row in range(0, h):
                for col in range(0, w):
                    if bg[row][col] == 255:
                        nn = 1
                        lifearea += 1
                        area(row, col)
                        life.append(nn)

            maxlife = max(life)
            indexmaxlife = life.index(maxlife)
            for row in range(0, h):
                for col in range(0, w):
                    bg[row][col] = 255 if bg[row][col] == indexmaxlife + 1 else 0
        real_shape.append(bg)

    # 圖片週圍加白色空白
    newH, newW = thresh.shape
    space = 8
    offset = 2
    bg = np.zeros((newH + space*2, newW + space*2 + nChar*3, 1), np.uint8)
    bg.fill(0)
    for i, letter in enumerate(real_shape):
        h, w = letter.shape
        x, y, _, _ = letterlist[i]
        for row in range(h):
            for col in range(w):
                bg[space + y + row, space + x + col + i*offset] = letter[row, col]
    _, bg = cv2.threshold(bg, 127, 255, cv2.THRESH_BINARY_INV)

    # 儲存處理後圖片
    cv2.imwrite(output_path, bg)
    print(f"處理完成: {output_path}")

print("所有圖片處理完成！")

###############################################################################################


# 設定圖片來源資料夾
input_folder = r".\\car\\processed"

# OCR 辨識車牌的主程式
def process_images(folder_path):
    # 確認 OCR 工具是否可用
    tools = pyocr.get_available_tools()
    if len(tools) == 0:
        print("No OCR tool found")
        sys.exit(1)
    tool = tools[0]  # 取得可用工具

    # 確認資料夾存在
    if not os.path.exists(folder_path):
        print(f"資料夾不存在: {folder_path}")
        return

    # 讀取資料夾內的所有圖片檔案
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    if not image_files:
        print("資料夾中沒有圖片檔案")
        return

    # 處理每張圖片
    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)
        print(f"處理圖片: {image_path}")

       # 讀取圖片
        image = cv2.imread(image_path)
        if image is None:
            print(f"無法讀取圖片: {image_path}")
            continue

        try:
            # OCR 辨識
            result = tool.image_to_string(
                Image.open(image_path),
                builder=pyocr.builders.TextBuilder()
            )

            # 優化 OCR 結果
            txt = result.replace("!", "1")  # 如果是 ! 字元，更改為字元 1
            real_txt = re.findall(r'[A-Z]+|[\d]+', txt)  # 只取數字和大寫英文字母

            # 組合真正的車牌
            txt_Plate = "".join(real_txt)

            print("OCR 辨識結果：", result)
            print("優化後辨識結果：", txt_Plate)

        except Exception as e:
            print(f"OCR 辨識失敗: {e}")
            continue

        # 顯示圖片
        cv2.imshow('image', image)
        cv2.moveWindow("image", 500, 250)  # 將視窗移到指定位置
        key = cv2.waitKey(0)  # 按任意鍵結束當前圖片的顯示
        cv2.destroyAllWindows()

# 呼叫主程式
process_images(input_folder)
