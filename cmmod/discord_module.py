import discord

class CustomEmbed():
    def __init__(self) -> None:
        pass

    #通常
    def default(self, title:str, description:str, color=0x0067C0) -> discord.Embed:
        embed=discord.Embed(title=title,description=description, color=color)
        return embed

    #完了
    def success(self, description:str) -> discord.Embed:
        embed=discord.Embed(description=description,color=0x2CA02C)
        embed.set_author(name='完了', icon_url='https://icons.veryicon.com/png/o/miscellaneous/8atour/success-35.png')
        return embed

    #エラー
    def error(self, description:str) -> discord.Embed:
        embed=discord.Embed(description=description,color=0xEC1A2E)
        embed.set_author(name='エラー', icon_url='https://cdn0.iconfinder.com/data/icons/shift-free/32/Error-512.png')
        return embed

    #待機中
    def waiting(self, description:str) -> discord.Embed:
        embed=discord.Embed(description=description,color=0x73A1FB)
        embed.set_author(name='待機中', icon_url='https://cdn-icons-png.flaticon.com/512/248/248958.png')
        return embed

    #注意
    def caution(self, description:str) -> discord.Embed:
        embed=discord.Embed(description=description,color=0xFF983F)
        embed.set_author(name='注意', icon_url='https://www.freeiconspng.com/thumbs/warning-icon-png/orange-warning-icon-3.png')
        return embed

    #通常(フィールド追加)
    def default_withfields(self, title:str, description:str, *fields:list, color=0x0067C0) -> discord.Embed:
        embed=discord.Embed(title=title, description=description, color=color)
        for field in fields: embed.add_field(name=field["name"], value=field["value"], inline=field["inline"])
        return embed