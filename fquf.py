from typing import Union
from database import Database, DiscordDatabase
import requests
import io
import aiohttp
            
class DatabaseFunction():
    def __init__(self):
        self.db = Database()
        self.dcdb = DiscordDatabase()
        self.cmf = CommonFunction()

    #ワールド情報取得
    async def get_worlddata(self, guild_id:int) -> list:
        wd = await self.db.get_db(name='read', table='world-master', column='guild_id', record=str(guild_id), recordtype='str') #ワールド情報GET
        return wd
    
    #地図情報取得
    async def get_mapdata(self, guild_id:int, column:str, record:Union[str,int], recordtype:str) -> list:
        md = await self.db.get_db(name='read', table=f'map-master[{str(guild_id)}]', column=column, record=record, recordtype=recordtype) #地図情報GET
        return md
    
    #地図情報送信
    async def post_mapdata(self, postdata:dict, guild_id:int, column:str, record:Union[str,int], apptype:int) -> requests.Response:
        r = await self.db.post_db(name='write', data=postdata, table=f'map-master[{str(guild_id)}]', column=column, record=record, apptype=apptype) #地図情報POST
        return r
    
    #地図情報ログ送信
    async def log_mapdata(self, logdata:dict, guild_id:int) -> requests.Response:
        r = await self.db.post_db(name='log', data=logdata, table=f'map-log[{str(guild_id)}]') #地図情報ログPOST
        return r
    
    #URLから画像GET処理
    async def get_image(self, image_url:str) -> bytes:
        async with aiohttp.ClientSession() as session:
            async with session.get(url=image_url) as r:
                b = await r.content.read()
                return b

class CommonFunction():
    def __init__(self) -> None:
        pass

    def create_map_id(self, m:int, x:int, z:int) -> str:
        map_id = f'M{str(m)}X{str(x)}Z{str(z)}'
        return map_id
    
    def pilbytesio(self, image) -> io.BytesIO:
        fileio = io.BytesIO()
        image.save(fileio,format='png')
        fileio.seek(0)
        return fileio
    