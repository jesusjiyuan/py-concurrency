import cv2
import numpy as np

ifile = "C:\\Users\\user\\Desktop\\bizjar\\20240117142630.jpg"
ofile = "C:\\Users\\user\\Desktop\\bizjar\\20240117142630_1.jpg"

def demo1():
    # 加载原始图像
    image = cv2.imread(ifile)

    # 创建一个Mask对象，将其设置为与输入图像相同大小且全黑色（0）
    mask = np.zeros(image.shape[:2], dtype=np.uint8)

    # 定义前景区域的ROI（Region of Interest）
    roi = cv2.selectROI("Select ROI", image)
    x, y, w, h = roi
    cv2.rectangle(mask, (int(x), int(y)), (int(x + w), int(y + h)), (255), -1)

    # 应用Mask到原始图像上，得到只包含前景部分的新图像
    result = cv2.bitwise_and(image, mask)

    # 显示结果图像
    cv2.imshow("Result Image", result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def demo2():
    from PIL import Image
    import rembg
    img = Image.open(ofile)#准备修改的图片路径
    img_bg_remove = rembg.remove(img)
    img_bg_remove = img_bg_remove.convert('RGB')
    #如果需要保存为jpg或者jpeg格式则需要使用此行代码，使用后背景为黑色
    img_bg_remove.save(ofile)#修改后保存的图片路径

def demo3():
    # 导入库
    bimage = "C:\\Users\\user\\Desktop\\bizjar\\wihte.png"
    import os
    #os.system(f'backgroundremover -m u2net -bi {bimage} -i {ifile} -o {ofile}')
    os.system(f'backgroundremover -m u2netp -i {ifile} -o {ofile}')


demo3()