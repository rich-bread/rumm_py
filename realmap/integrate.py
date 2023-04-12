import io
from PIL import Image
from fquf import DatabaseFunction, CommonFunction

class Integrate():
    def __init__(self):
        self.length = 128
        self.dbf = DatabaseFunction()
        self.cmf = CommonFunction()

    #左上X,Zと右下X,Zの座標を取得
    def get_xzulbr(self, mapdata:list) -> list:
        xl = []
        zl = []
        for md in mapdata:
            xl.append(md[3])
            zl.append(md[4])
        xzulbr = [min(xl),min(zl),max(xl),max(zl)]
        return xzulbr
    
    async def make_img2d_list(self, rmd:list, ml:int, xul:int, zul:int, xbr:int, zbr:int) -> list:
        mdmid = [md[1] for md in rmd]
        print(mdmid)
        img2d_list = []
        for z in range(zul,zbr+1):
            imgx_list = []
            for x in range(xul,xbr+1):
                map_id = self.cmf.create_map_id(m=ml, x=x, z=z)
                print(map_id)
                if map_id in mdmid:
                    i = mdmid.index(map_id)
                    iu = rmd[i][5]
                    ib = io.BytesIO(await self.dbf.get_image(iu))
                    imgx = Image.open(ib)
                else: imgx = Image.new('RGBA',(self.length,self.length))
                imgx_list.append(imgx)
            img2d_list.append(imgx_list)
        return img2d_list
    
    def get_x(self, img_list:list) -> Image:
        dst = Image.new('RGBA',(self.length*len(img_list),img_list[0].height))
        posx = 0
        for img in img_list:
            dst.paste(img,(posx,0))
            posx+=self.length
        return dst
    
    def get_z(self, img_list:list) -> Image:
        dst = Image.new('RGBA',(img_list[0].width,self.length*len(img_list)))
        posx = self.length*(len(img_list)-1)
        for img in img_list:
            dst.paste(img,(0,posx))
            posx-=self.length
        return dst
    
    #
    def integrate(self, img2d_list) -> Image:
        imgx = [self.get_x(img) for img in img2d_list]
        imgxz = self.get_z(imgx)
        return imgxz
    
    def reverse_integrate(self, img2d_list) -> Image:
        imgx = [self.get_x(img) for img in reversed(img2d_list)]
        imgxz = self.get_z(imgx)
        return imgxz