import discord
from discord.ext import commands
from discord import app_commands
from cmmod.json_module import open_json
from cmmod.error_module import MyError
from cmmod.discord_module import CustomEmbed
from fquf import DatabaseFunction, CommonFunction
from realmap.integrate import Integrate

cd = open_json(r'./static/go_integrate.json')

class GoIntegrate(commands.Cog):
    def __init__(self, client:discord.Client):
        self.client = client
        self.dbf = DatabaseFunction()
        self.cmf = CommonFunction()
        self.mitf = Integrate()
        self.custembed = CustomEmbed()

    @app_commands.command(name=cd['name'], description=cd['description'])
    @app_commands.describe(map_level=cd['describe']['map_level'])
    @app_commands.guild_only()
    async def go_integrate(self, interaction:discord.Interaction, map_level:int):
        try:
            await interaction.response.defer(thinking=True) #thinking処理

            raw_mapdata = await self.dbf.get_mapdata(guild_id=interaction.guild_id, column='map_level', record=map_level, recordtype='int')
            if not raw_mapdata[0]: raise MyError("指定した地図レベルの地図画像がデータベースに登録されていないよ！")
            xzulbr = self.mitf.get_xzulbr(mapdata=raw_mapdata)

            raw_worlddata = await self.dbf.get_worlddata(guild_id=interaction.guild_id)
            worlddata = raw_worlddata[0]
            integrate_mode = worlddata[4]

            img2d_list = await self.mitf.make_img2d_list(raw_mapdata, map_level, *xzulbr)
            if integrate_mode == 0: imgfig = self.mitf.integrate(img2d_list=img2d_list)
            elif integrate_mode == 1: imgfig = self.mitf.reverse_integrate(img2d_list=img2d_list)

        except MyError as e:
            await interaction.followup.send(content=interaction.user.mention, embed=self.custembed.error(description=str(e)))

        except Exception as e:
            em = "予期せぬエラーが発生してしまった...。管理者までお問い合わせください！\nエラー内容:"+str(e)
            print(em)
            await interaction.followup.send(content=interaction.user.mention, embed=self.custembed.error(em))

        else:
            fileio = self.cmf.pilbytesio(imgfig)
            await interaction.followup.send(file=discord.File(fileio,"integrate.png"))

async def setup(client:commands.Bot):
    await client.add_cog(GoIntegrate(client))
