from typing import Any, Optional, Union
import discord
from discord.emoji import Emoji
from discord.enums import ButtonStyle
from discord.interactions import Interaction
from discord.partial_emoji import PartialEmoji
import sales_finder
from api_locator import APILocator

class BoolParamsButton(discord.ui.Button):
    def __init__(self, param_name, style: ButtonStyle = ButtonStyle.secondary, label: Optional[str] = None, disabled: bool = False, custom_id: Optional[str] = None, url: Optional[str] = None,emoji: Optional[Union[str, Emoji, PartialEmoji]] = None, row: Optional[int] = None,):
        super().__init__(style=style, label=label, disabled=disabled, custom_id=custom_id, url=url, emoji=emoji, row=row)
        self.param_name = param_name
        self.enabled = False
        self.enabled_style = discord.ButtonStyle.primary
        self.disabled_style = discord.ButtonStyle.gray

    async def callback(self, interaction: discord.Interaction):
        self.enabled = not self.enabled
        self.label = str(self.label).replace('(enabled)', '(disabled)').replace('(disabled)', '(enabled)')
        self.style = self.enabled_style if self.enabled else self.disabled_style
        await interaction.response.edit_message(view=self.view)

class StoreSelect(discord.ui.Select):
    def __init__(self, *, placeholder: str = 'Select Stores', min_values: int = 1, max_values: int = 1, options: list[discord.SelectOption], custom_id: str = 'store_options', row: Optional[int] = None):
        super().__init__(placeholder=placeholder, min_values=min_values, max_values=max_values, options=options, custom_id=custom_id, row=row)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()

        def get_selected_values(option: discord.SelectOption):
            for selected_value in self.values:
                if option.value == selected_value:
                    return True
            return False
        for option in self.options:
            option.default = get_selected_values(option)

        await interaction.followup.edit_message(message_id=interaction.message.id, view=self.view)

        
def get_sort_options():
    ret = []

    for enum in APILocator.get_api().get_sort_options():
        title_str = str(enum.name).title().replace('_', ' ')
        value_str = str(enum.value)

        ret.append(discord.SelectOption(
            label=title_str,
            value=value_str,
            default=False
        ))

    return ret


def get_bool_params() -> list[BoolParamsButton]:
    if APILocator.get_api().get_bool_parameters():
        return list(map(lambda tuple: BoolParamsButton(param_name=tuple[1], custom_id=tuple[1], label=tuple[0] + ' (disabled)'), APILocator.get_api().get_bool_parameters().items()))
    return []

def pack_select_options(select_options: list[discord.SelectOption]) -> list[StoreSelect]:
    ret = []
    for i in range(0, len(select_options), 25):
        store_select = StoreSelect(
            options=select_options[i:min(i+25, len(select_options))],
            placeholder='Select Stores',
            min_values=1,
            custom_id='store_options_{0}'.format(i / 25)
        )
        store_select.max_values = len(store_select.options)
        ret.append(store_select)
    return ret

class SettingsView(discord.ui.View):

    _sort_options: discord.ui.Select
    _store_options: list
    _params: list
    
    def __init__(self):
        super().__init__(timeout=None)

        if not SettingsView._store_options:
            raise Exception('Store options not initialized')
     
        self._init_params()
        self._init_sort_options()
        self._init_store_options()

    @classmethod
    @property
    def filtered_stores(cls) -> list[discord.SelectOption]:
        ret = []
        for select in SettingsView._store_options:
            ret.extend(list(filter(lambda option: option.default, select.options)))
        return ret

    @classmethod
    @property
    def selected_sort_options(cls) -> list[discord.SelectOption]:
        return list(filter(lambda option: option.default, SettingsView._sort_options.options))
    
    @classmethod
    @property
    def params(cls):
        ret = {}
        for param in cls._params:
            ret[param.param_name] = str(int(param.enabled))
        return ret
    
    @discord.ui.button(label='Reset filter', style=discord.ButtonStyle.red, custom_id='sw_b_reset_filter', row=4)
    async def reset_filter(self, interaction: discord.Interaction, button: discord.ui.Button):
        for select in SettingsView._store_options:
            for select_option in select.options:
                select_option.default = False
        await interaction.response.edit_message(view=self)

    def _init_params(self):
        for params in SettingsView._params:
            params.row = 4
            self.add_item(params)

    def _init_sort_options(self):
        async def sort_options(interaction: discord.Interaction):
            if SettingsView._sort_options.values:
                value = SettingsView._sort_options.values[0]
                if value not in [sort_option.value for sort_option in APILocator.get_api().get_sort_options()]:
                    await interaction.response.send_message('API does not support this sort option', ephemeral=True)
                    raise Exception('API does not supported this sort option')
                
                for option in SettingsView._sort_options.options:
                    option.default = False

                for option in SettingsView._sort_options.options:
                    if option.value == value:
                        option.default = True
                        break

            await interaction.response.defer()
            
        SettingsView._sort_options.callback = sort_options
        SettingsView._sort_options.row = 1  
        self.add_item(SettingsView._sort_options)

    def _init_store_options(self):
        for i, store_select in enumerate(SettingsView._store_options):
            store_select.row = 2 + i
            self.add_item(store_select)

    @classmethod
    def init_class_attributes(cls):
        cls._sort_options = discord.ui.Select(
            options=get_sort_options(),
            placeholder='Sort Options',
            min_values=1, max_values=1,
            custom_id='sort_options',
        )

        cls._sort_options.options[0].default = True

        cls._store_options = pack_select_options(list(map(lambda store: discord.SelectOption(label=store.name, value=store.id, emoji='🛒'), APILocator.get_api().fetch_game_stores())))
        cls._params  = get_bool_params()