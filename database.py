import os
import io
import json
import requests
import aiohttp
import discord
from typing import Union

class Database():
    def __init__(self) -> None:
        self.url = os.getenv('GAS_PROJECT_URL')+'?'

    #DBへのPOST処理
    async def post_db(self, name:str, data:dict, **kwargs) -> requests.Response:
        base = {'name':name}
        payload = base|kwargs
        res = requests.post(url=self.url, params=payload, data=json.dumps(data))
        return res

    #DBへのGET処理
    async def get_db(self, name:str, **kwargs) -> Union[dict,list]:
        base = {'name':name}
        async with aiohttp.ClientSession() as session:
            async with session.get(url=self.url, params=base|kwargs) as resp:
                resj = await resp.json()
                return resj
            
class DiscordDatabase():
    def __init__(self) -> None:
        pass
    
    #DiscordDatabaseサーバーへの画像POST処理(一括)
    async def post_image(self, channel:discord.TextChannel, image:discord.Attachment, filename:str, content:str=None) -> str:
        imgby = await image.read() #bytes型で添付ファイルを取得
        imgbyio = io.BytesIO(imgby) #BytesIO型に変換
        file = discord.File(fp=imgbyio, filename=filename) #discord.Fileで添付ファイルを新規作成
        msg = await channel.send(content=content,file=file) #添付ファイル送信
        url = msg.attachments[0].url
        return url
    
    #DiscordDatabaseサーバーへの画像POST処理(受取のみ)
    async def post_iimage(self, channel:discord.TextChannel, image:io.BytesIO, filename:str, content:str=None) -> str:
        file = discord.File(fp=image, filename=filename) #discord.Fileで添付ファイルを新規作成
        msg = await channel.send(content=content,file=file) #添付ファイル送信
        url = msg.attachments[0].url
        return url
    