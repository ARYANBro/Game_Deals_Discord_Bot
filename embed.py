import discord
from datetime import datetime
from sales_finder import game_sales

def short_description(description: str) -> str:
    if len(description) > 200:
        return description[:200] + '...'
    return description

def quote(string: str) -> str:
    new_str = '>>> ' + string
    return new_str

def create_embed(game_info):
    game_embed = discord.Embed(
        title=game_info['title'],
        url=game_info['store_link'],
        description=quote(short_description(game_info['description'])),
        color=discord.Color.dark_theme(),
        timestamp=datetime.now()
    )

    game_embed.set_footer(text="CheapShark for sales, RAWG for images and game info")
    game_embed.set_author(name=game_info['store_name'])
    game_embed.set_image(url=game_info['game_cover'])
    game_embed.add_field(name='`💰 Savings`', value=game_info['savings'], inline=True)
    game_embed.add_field(name='`🥇 Metacritic Rating`', value=game_info['metacritic_rating'], inline=True)
    return game_embed