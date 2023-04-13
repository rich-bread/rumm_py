import discord
from discord.ext import commands
from discord import app_commands
from fquf import DatabaseFunction, CommonFunction
from cmmod.json_module import open_json
from cmmod.discord_module import CustomEmbed
from cmmod.error_module import MyError

cd = open_json(r'./static/get_map.json')
cddb = cd['describe']

class GetMap(commands.Cog):
    def __init__(self, client:discord.Client):
        self.client = client
        self.dbf = DatabaseFunction()
        self.cmf = CommonFunction()
        self.custembed = CustomEmbed()

    @app_commands.command(name=cd['name'],description=cd['description'])
    @app_commands.describe(map_level=cddb['map_level'],x_number=cddb['x_number'],z_number=cddb['z_number'])
    async def get_map(self, interaction:discord.Interaction, map_level:int, x_number:int, z_number:int):
        try:
            await interaction.response.defer(thinking=True) #thinking処理
            
            map_id = self.cmf.create_map_id(m=map_level,x=x_number,z=z_number) #地図ID作成
            raw_mapdata = await self.dbf.get_mapdata(guild_id=interaction.guild_id, column='map_id', record=map_id, recordtype='str') #地図情報リクエスト
            mapdata = raw_mapdata[0]

            if not mapdata: raise MyError("指定した地図画像はデータベースに登録されてないよ！")

        except MyError as e:
            await interaction.followup.send(content=interaction.user.mention, embed=self.custembed.error(description=str(e)))
        
        except Exception as e:
            em = "予期せぬエラーが発生しました。お手数ですが管理者までお問い合わせください\nエラー内容:"+str(e)
            print(em)
            await interaction.followup.send(content=interaction.user.mention, embed=self.custembed.error(em))
        
        else:
            image_url = mapdata[5] #地図画像URL
            sm = f"指定地図画像[{str(map_level)},{str(x_number)},{str(z_number)}]を以下に添付しました"
            await interaction.followup.send(content=interaction.user.mention+'\n'+image_url, embed=self.custembed.success(sm))

async def setup(client:commands.Bot):
    await client.add_cog(GetMap(client))
