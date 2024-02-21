import os
import json
import shutil

import cv2
import requests
import matplotlib.pyplot as plt

CONFIG_FP = os.path.join(os.path.dirname(__file__), "config.json")


def get_config(config_fp=CONFIG_FP):
    with open(config_fp) as f:
        config = json.load(f)

    return config


def crop_image(x1, y1, x2, y2, image_path, output_path):
    # 读取图片
    img = cv2.imread(image_path)
    # 切割图片
    cropped_img = img[y1:y2, x1:x2]
    # 保存切割后的图片
    cv2.imwrite(output_path, cropped_img)


def get_subimage_clarity(image_fp, threshold=250):
    image = (plt.imread(image_fp) * 255).astype("uint8")
    std = image.std()
    span = image.max() - image.min()

    score = std * span
    if score > threshold:
        return True
    else:
        return False


def analysis_visibility(image_fp, threshold=250, tmpdir="./tmp", keep_tmp=False):
    config = get_config()
    visibles = []
    for key, value in config.items():
        x1, y1, x2, y2 = value["x1"], value["y1"], value["x2"], value["y2"]
        distance = value["distance"]
        savefp = os.path.join(tmpdir, f"{key}.jpg")
        os.makedirs(tmpdir, exist_ok=True)
        crop_image(x1, y1, x2, y2, image_fp, savefp)
        if get_subimage_clarity(savefp, threshold):
            visibles.append(distance)

    if not keep_tmp:
        shutil.rmtree(tmpdir)

    return round(max(visibles), 0)


if __name__ == "__main__":
    image_fp = "./iap-tower-camera.jpg"
    resp = requests.get(
        "http://view.iap.ac.cn:8080/imageview/northeast.jpg", stream=True
    )
    if resp.ok:
        with open(image_fp, "wb") as f:
            f.write(resp.content)

    visibility = analysis_visibility(image_fp)

    print(f"基于 IAP 铁塔照片反算当前北京市的能见度为 {visibility} km")
