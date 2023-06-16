import discord
from datetime import datetime
import sales_finder


class GameListView(discord.ui.View):
    def __init__(self, list_items, embed: discord.Embed):
        super().__init__()
        self.embed = embed
        self.list_items = list_items
        self.curr_index = 0        
        self.disabled_button.label = f'{self.curr_index + 1}/{len(self.list_items)}'
        
    @discord.ui.button(label='<<', style=discord.ButtonStyle.blurple)
    async def on_first_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.curr_index != 0:
            self.curr_index = 0
        
        await self._update(interaction)

    @discord.ui.button(label='<', style=discord.ButtonStyle.blurple)
    async def on_previous(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.curr_index != 0:
            self.curr_index -= 1
        
        await self._update(interaction)

    @discord.ui.button(label='>', style=discord.ButtonStyle.green)
    async def on_next(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.curr_index != len(self.list_items) - 1:
            self.curr_index += 1
        
        await self._update(interaction)

    @discord.ui.button(label='>>', style=discord.ButtonStyle.green)
    async def on_last_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.curr_index != len(self.list_items) - 1:
            self.curr_index = len(self.list_items) - 1
        
        await self._update(interaction)

    @discord.ui.button(disabled=True, style=discord.ButtonStyle.gray)
    async def disabled_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        pass


    async def _update(self, interaction: discord.Interaction):
        self.disabled_button.label = f'{self.curr_index + 1}/{len(self.list_items)}'

        self.embed.title = self.list_items[self.curr_index]['title']
        self.embed.description = self.list_items[self.curr_index]['description']
        self.embed.color = discord.Color.random()
        self.embed.timestamp = datetime.now()

        self.embed.set_image(url=self.list_items[self.curr_index]['game_cover'])

        stores = sales_finder.game_sales.get_stores()
        store_logo_url = 'https://www.cheapshark.com' + stores[int(self.list_items[self.curr_index]['store_id']) - 1]['images']['logo']
        self.embed.set_thumbnail(url=store_logo_url)

        self.embed.set_field_at(0, name="Savings", value=str(int(float(self.list_items[self.curr_index]["savings"]))) + '%', inline=True)
        self.embed.set_field_at(1, name="Store", value=sales_finder.game_sales.get_store_name(self.list_items[self.curr_index]["store_id"]), inline=True)
        self.embed.set_field_at(2, name=f"", value=f"[**Buy Now!**]({self.list_items[self.curr_index]['store_link']})", inline=False)

        await interaction.response.edit_message(embed=self.embed, view=self)
