import discord
from datetime import datetime
import sales_finder
from embed import create_embed


class GameListView(discord.ui.View):
    def __init__(self, list_items, embed: discord.Embed,):
        super().__init__()
        self.embed = embed
        self.list_items = list_items
        self.curr_index = 0        
        self.disabled_button.label = f'{self.curr_index + 1}/{len(self.list_items)}'

        self.buy_now = discord.ui.Button(style=discord.ButtonStyle.link, label='Buy Now', url=self.list_items[self.curr_index]['store_link'])
        self.add_item(self.buy_now)
        
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
        await interaction.response.defer()

    async def _update(self, interaction: discord.Interaction):
        self.disabled_button.label = f'{self.curr_index + 1}/{len(self.list_items)}'
        self.buy_now.url = self.list_items[self.curr_index]['store_link']
        self.embed = create_embed(self.list_items[self.curr_index], sales_finder.game_sales.get_stores())
        await interaction.response.edit_message(embed=self.embed, view=self)
