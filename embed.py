import discord
from datetime import datetime

def short_description(description: str) -> str:
    if len(description) > 200:
        return description[:200] + '...'
    return description

def quote(string: str) -> str:
    new_str = '>>> ' + string
    return new_str

def create_embed(game_info, stores):
    game_embed = discord.Embed(
        title=game_info['title'],
        description=quote(short_description(game_info['description'])),
        color=discord.Color.dark_theme(),
        timestamp=datetime.now()
    )

    game_embed.set_footer(text="Footer text here")
    game_embed.set_image(url=game_info['game_cover'])
    store_logo_url = 'https://www.cheapshark.com' + stores[int(game_info['store_id']) - 1]['images']['logo']
    game_embed.set_thumbnail(url=store_logo_url)
    game_embed.add_field(name='`💰 Savings`', value=game_info['savings'], inline=True)
    game_embed.add_field(name='`🥇 Metacritic Rating`', value=game_info['metacritic_rating'], inline=True)
    return game_embed