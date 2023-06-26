import discord
import sales_finder

class SettingsView(discord.ui.View):
    filtered_stores = []
    sort_by = str()
    only_aaa = False
    on_sale = False

    _select_options1 = []
    _select_options2 = []
    
    for i, store in enumerate(sales_finder.game_sales.get_stores()):
        if i == 25:
            break
        _select_options1.append(
            discord.SelectOption(
                label=store['storeName'],
                value=store['storeID'],
                emoji='🛒',
            )
        )
        
    for store in sales_finder.game_sales.get_stores()[25:]:
        _select_options2.append(
            discord.SelectOption(
                label=store['storeName'],
                value=store['storeID'],
                emoji='🛒',
            )
        )
    
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.select(placeholder='Filter options 1', min_values=1, max_values=len(_select_options1), options=_select_options1, custom_id='sw_filter_select_01')
    async def filter_select(self, interaction: discord.Interaction, select: discord.ui.Select):
        if select.values:
            SettingsView.filtered_stores.extend(select.values)

        self._filter_update_defaults(select.values, self._select_options1)
        await interaction.response.defer()

    @discord.ui.select(placeholder='Filter options 2', max_values=len(_select_options2), options=_select_options2, custom_id='sw_filter_select_02')
    async def filter_select2(self, interaction: discord.Interaction, select: discord.ui.Select):
        if select.values:
            SettingsView.filtered_stores.extend(select.values)
            
        self._filter_update_defaults(select.values, self._select_options2)
        await interaction.response.defer()    

    @discord.ui.select(placeholder='Sort By', options=[
        discord.SelectOption(label='Deal Rating', value='Deal Raiting'),
        discord.SelectOption(label='Savings', value='Savings'),
        discord.SelectOption(label='Price', value='Price'),
        discord.SelectOption(label='Metacritic', value='Metacritic'),
        discord.SelectOption(label='Reviews', value='Reviews'),
        discord.SelectOption(label='Release', value='Release'),
        discord.SelectOption(label='Store', value='Store'),
        discord.SelectOption(label='Recent', value='Recent'),
    ], custom_id='sw_sort_select')
    async def sort_select(self, interaction: discord.Interaction, select: discord.ui.Select):

        for option in self.sort_select.options:
            option.default = False

            if option.value == select.values[0]:
                option.default = True

        SettingsView.sort_by = select.values[0]

        await interaction.response.defer()

    # ! Buggy, color of button is not consistent
    @discord.ui.button(label='Allow AAA games', style=discord.ButtonStyle.blurple, custom_id='sw_b_aaa_games_only')
    async def aaa_games_only(self, interaction: discord.Interaction, button: discord.ui.Button):
        button.label = 'Allow all games' if button.label == 'Allow AAA games' else 'Allow AAA games'
        button.style = discord.ButtonStyle.blurple if button.label == 'Allow AAA games' else discord.ButtonStyle.green
        SettingsView.only_aaa = not SettingsView.only_aaa
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label='Reset filter', style=discord.ButtonStyle.red, custom_id='sw_b_reset_filter')
    async def reset_filter(self, interaction: discord.Interaction, button: discord.ui.Button):
        SettingsView.filtered_stores = []
        for select_option in self._select_options1:
            select_option.default = False
        await interaction.response.edit_message(view=self)

    # ! Buggy, color of button is not consistent
    @discord.ui.button(label='Show  sale only', style=discord.ButtonStyle.blurple, custom_id='sw_b_on_sale_only')
    async def on_sale_only(self, interaction: discord.Interaction, button: discord.ui.Button):
        button.label = 'Show all games' if button.label == 'Show sale only' else 'Show sale only'
        button.style = discord.ButtonStyle.blurple if button.label == 'Show sale only' else discord.ButtonStyle.green
        SettingsView.on_sale = not SettingsView.on_sale
        await interaction.response.edit_message(view=self)

    def _filter_update_defaults(self, selected_values, select_options):
        # ! Buggy, for some reason some values are removed when a button is pressed
        selected_values = sorted(selected_values)

        for select_option in select_options:
            select_option.default = False

        search_idx = 0
        for select_option in select_options:

            if search_idx == len(selected_values):
                break

            for value in selected_values[search_idx:]:
                if value == select_option.value:
                    select_option.default = True
                    search_idx += 1
                    break
