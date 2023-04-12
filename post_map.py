import discord
from discord.ext import commands
from discord import app_commands
from database import DiscordDatabase
from fquf import DatabaseFunction, CommonFunction
from cmmod.json_module import open_json
from cmmod.discord_module import CustomEmbed
from cmmod.time_module import get_currenttime
from realmap.detect import Detect

cd = open_json(r'./static/post_map.json')
cddb = cd['describe']

class PostMap(commands.Cog):
    def __init__(self, client:discord.Client):
        self.client:discord.Client = client
        self.dbf = DatabaseFunction()
        self.cmf = CommonFunction()
        self.dcdb = DiscordDatabase()
        self.mdtf = Detect()
        self.custembed = CustomEmbed()

    @app_commands.command(name=cd['name'],description=cd['description'])
    @app_commands.describe(map_level=cddb['map_level'],x_number=cddb['x_number'],z_number=cddb['z_number'])
    async def post_map(self, interaction:discord.Interaction, map_level:int, x_number:int, z_number:int, image:discord.Attachment):
        try:
            await interaction.response.defer(thinking=True) #thinking処理

            imgmap = await self.mdtf.detect_map_fromimage(image) #地図画像切り取り処理
            
            map_id = self.cmf.create_map_id(m=map_level, x=x_number, z=z_number) #地図ID作成
            raw_mapdata = await self.dbf.get_mapdata(guild_id=interaction.guild_id, column='map_id', record=map_id, recordtype='str') #地図情報取得
            mapdata = raw_mapdata[0]
            if not mapdata: apptype = 0
            else: apptype = 1

            raw_worlddata = await self.dbf.get_worlddata(guild_id=interaction.guild_id) #ワールド情報取得
            worlddata = raw_worlddata[0]
            dbid = worlddata[3] #DiscordDatabaseチャンネルID
            dbchannel = await self.client.fetch_channel(int(dbid)) #DiscordDatabaseチャンネル取得
            filename = map_id+'.png' #ファイル名作成
            image_url = await self.dcdb.post_iimage(channel=dbchannel,image=imgmap,filename=filename) #画像POST
            currenttime = get_currenttime() #現在日時取得

            postdata = {"map_id":map_id, "map_level":map_level, "x_number":x_number, "z_number":z_number, "image_url":image_url, "datetime":currenttime} #POST情報作成
            logdata = postdata|{"author_name":str(interaction.user), "author_id":str(interaction.user.id)} #ログ情報作成
            await self.dbf.post_mapdata(postdata=postdata, guild_id=interaction.guild_id, column='map_id', record=map_id, apptype=apptype) #POST処理
            await self.dbf.log_mapdata(logdata=logdata, guild_id=interaction.guild_id) #ログ記入

        except Exception as e:
            em = "予期せぬエラーが発生してしまった...。管理者までお問い合わせください！\nエラー内容:"+str(e)
            print(em)
            await interaction.followup.send(content=interaction.user.mention, embed=self.custembed.error(em))

        else:
            sm = f"添付地図画像を[{str(map_level)},{str(x_number)},{str(z_number)}]として登録したよ！"
            await interaction.followup.send(content=interaction.user.mention, embed=self.custembed.success(sm))

async def setup(client:commands.Bot):
    await client.add_cog(PostMap(client))
