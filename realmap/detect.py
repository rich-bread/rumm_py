import io
import cv2
import numpy
import PIL
from PIL import Image
import discord

class Detect():
    def __init__(self) -> None:
        self.length = 128

    def cv2pil(self, image:numpy.ndarray):
        #OpenCV型 -> PIL型
        new_image = image.copy()
        if new_image.ndim == 2:  # モノクロ
            pass
        elif new_image.shape[2] == 3:  # カラー
            new_image = cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB)
        elif new_image.shape[2] == 4:  # 透過
            new_image = cv2.cvtColor(new_image, cv2.COLOR_BGRA2RGBA)
        new_image = Image.fromarray(new_image)
        return new_image

    def detect_map(self, imgby:bytes):
        #　bytesからcv2に画像を読み込み
        imgbyio = io.BytesIO(imgby)
        img = cv2.imdecode(numpy.frombuffer(imgbyio.read(), numpy.uint8),1)

        # BGR->HSV変換
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # 地図枠の色範囲
        #（BGRで[148, 188,211]と[107, 133, 151]）
        # print(cv2.cvtColor(np.uint8([[[148, 188,211]]]), cv2.COLOR_BGR2HSV))
        lower = numpy.array([17,70,125])
        upper = numpy.array([19,90,220])

        # Threshold the HSV image to get only colors
        mask = cv2.inRange(hsv, lower, upper)
        mask = cv2.bitwise_not(mask)

        #マスク画像から輪郭を探す
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

        #地図枠の候補をリストアップ
        flame_can = []
        for i in range(0, len(contours)):
            if len(contours[i]) > 0:
                #remove small objects
                if cv2.contourArea(contours[i]) < 10000 or cv2.contourArea(contours[i]) > 1500000:
                    continue

                rect = contours[i]
                flame_can.append(cv2.boundingRect(rect))

        w_can = [row[2] for row in flame_can]
        w=min(w_can)
        flame = flame_can[w_can.index(w)]
        x,y,w,h= flame
        l = min([w,h])

        pil_img = self.cv2pil(img)
        pil_img = pil_img.crop((x,y,x+l,y+l))
        pil_img = pil_img.resize((128,128), 0)
        return pil_img
    
    async def detect_map_fromimage(self, image:discord.Attachment) -> io.BytesIO:
        imgby = await image.read()
        imgmap = self.detect_map(imgby)
        fileio = io.BytesIO()
        imgmap.save(fileio,format='png')
        fileio.seek(0)
        return fileio