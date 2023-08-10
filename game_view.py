import discord
from embed import create_embed


class GameListView(discord.ui.View):
    def __init__(self, embeds: list[discord.Embed]):
        super().__init__()
        self.embeds = embeds
        self.curr_index = 0        
        self.disabled_button.label = f'{self.curr_index + 1}/{len(self.embeds)}'
        self.timeout = None

    @discord.ui.button(label='<<', style=discord.ButtonStyle.blurple, custom_id='glv_b_on_first_page')
    async def on_first_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.curr_index != 0:
            self.curr_index = 0
        await self._update(interaction)

    @discord.ui.button(label='<', style=discord.ButtonStyle.blurple, custom_id='glv_b_on_previous')
    async def on_previous(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.curr_index != 0:
            self.curr_index -= 1
        await self._update(interaction)

    @discord.ui.button(label='>', style=discord.ButtonStyle.green, custom_id='glv_b_on_next')
    async def on_next(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.curr_index != len(self.embeds) - 1:
            self.curr_index += 1
        await self._update(interaction)

    @discord.ui.button(label='>>', style=discord.ButtonStyle.green, custom_id='glv_b_on_last_page')
    async def on_last_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.curr_index != len(self.embeds) - 1:
            self.curr_index = len(self.embeds) - 1
        await self._update(interaction)

    @discord.ui.button(disabled=True, style=discord.ButtonStyle.gray, custom_id='glv_b_disabled_button')
    async def disabled_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()

    async def _update(self, interaction: discord.Interaction):
        self.disabled_button.label = f'{self.curr_index + 1}/{len(self.embeds)}'
        embed = self.embeds[self.curr_index]
        await interaction.response.edit_message(embed=embed, view=self)
