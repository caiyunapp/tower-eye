# tower-eye
本项目的主要工作是基于中科院大气物理研究所的[气象观测塔](http://view.iap.ac.cn:8080/imageview/)上的相机拍摄的照片反算能见度。
![](./data/clear.jpg)

## 快速开始
要运行本项目，需要先将仓库克隆到本地
```bash
$ git clone https://github.com/caiyunapp/tower-eye.git
```
安装依赖
```bash
$ pip install -r requirements.txt
```
运行样例：
```bash
$ python towereye.py
基于 IAP 铁塔照片反算当前北京市的能见度为 19.0 km
```
如果想要测试其他时刻的照片，可以参考以下代码：
```python
from towereye import analysis_visibility

image_fp = "./iap-tower-camera.jpg"  # 替换为你下载的 IAP 铁塔的照片（须为东北方向）

visibility = analysis_visibility(image_fp)

print(f"基于 IAP 铁塔照片反算当前北京市的能见度为 {visibility} km")
```

大道至简，顶级的算法只需要最朴素的处理方式 🤫
