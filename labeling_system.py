from PIL import Image
import numpy as np
import cv2
from pymongo import MongoClient, errors
import random
import os

import warnings
warnings.simplefilter("ignore", Image.DecompressionBombWarning)


collection = None
def set_env(host, db_name, collection_name):
    global client, db, collection

    client =  MongoClient(host)
    db = client[db_name]
    collection = db[collection_name]

def read_image(path):
    img = Image.open(path)
    img = img.convert('RGB')
    return np.array(img, dtype=np.uint8)

def save_pause_point(path, index):
    with open('pause.txt', 'w') as f:
        f.write(f"{path}\n{index}")

def get_window_size(img):
    height, width, _ = img.shape

    # 적절한 윈도우 크기 계산
    max_width = 1280
    max_height = 1020
    scale = min(max_width / width, max_height / height)
    window_width = int(width * scale)
    window_height = int(height * scale)

    return window_height, window_width

def get_datas(sample_num):
    cursor = collection.find({"label":None})
    datas = list(cursor)
    datas = random.choices(datas, k=sample_num)
    return datas

def make_path(data):
    path = os.path.join("/",
                data["start_path"],
                data["HDD_name"],
                data["middle_path"],
                data["tag"][0],
                data["file_name"]
            )
    return path

def open_cv():
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
def close_cv():
    cv2.destroyAllWindows()

def run(data=None):
    if data == None:
        return 0

    try:
        img_path = make_path(data)
        img = read_image(img_path)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        height, width = get_window_size(img)

        cv2.resizeWindow('image', width, height)

        cv2.imshow('image', img)

        k = cv2.waitKey(0)
        
        if k == ord('d'):
            # 제품 True
            collection.update_one({"_id":data["_id"]}, {"$set": {"label": "product"}})
        elif k == ord('a'):
            # 비제품 False
            collection.update_one({"_id":data["_id"]}, {"$set": {"label": "non_product"}})
        elif k == ord('s'):
            # 의류(모델이 입고 찍은)
            collection.update_one({"_id":data["_id"]}, {"$set": {"label": "with_model"}})
        elif k == ord('z'):
            return 2
        elif k == ord('p'):
            return 0
    except:
        return 1
    return 1

if __name__ == "__main__":
    
    set_env("mongodb://localhost:27018/","DBproduct_eng","product_detection_data")
    datas = get_datas(100)
    
    open_cv()

    index = 0
    while index <= len(datas):
        state = run(datas[index])

        if state == 2:
            index -= 1
        elif state == 1:
            index += 1
        elif state == 0:
            break

    close_cv()

