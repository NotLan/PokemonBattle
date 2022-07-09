from ottermation.plugins.playwright import AbstractPage
from pyotp import random

from page_objects.battle_page import BattlePage


class PvPokePage(AbstractPage):

    add_pokemon_button = 'text=+ Add Pokemon >> nth=0'
    add_selected_pokemon_button = '.save-poke'
    search_text_field = 'text=Random Swap Select a Pokemon AbomasnowAbomasnow (Mega)Abomasnow (Shadow)AbraAbra >> [placeholder="Search name"]'
    pick_pokemon_dropdown = 'text=Random Swap Select a Pokemon AbomasnowAbomasnow (Mega)Abomasnow (Shadow)AbraAbra >> select >> nth=0'
    pokemon_selection_dropdown = 'text=Random Swap Select a Pokemon AbomasnowAbomasnow (Mega)Abomasnow (Shadow)AbraAbra >> select >> nth=0'
    battle_button = 'button:has-text("Battle")'

    league_dropdown = '.league-cup-select'
    difficulty_dropdown = '.difficulty-select'
    auto_tap_button = 'text=Autotap >> nth=0'
    no_shields = '.option >> nth=0'
    no_oppenent_shield = 'div:nth-child(2) > .poke-stats > .options > .shield-section > .form-group > div >> nth=0'
    random_button = 'text=Random >> nth=1'

    url = 'https://pvpoke.com/battle/'

    def go_to_site(self):
        """

        :return:
        """
        self.page.goto(self.url, wait_until="networkidle")
        return PvPokePage

    def click_opponent_random(self):
        self.page.click(self.random_button)

    def click_no_opponent_shield(self):
        self.page.click(self.no_oppenent_shield)

    def click_no_shields(self):
        self.page.click(self.no_shields)

    def click_auto_tap(self):
        self.page.click(self.auto_tap_button)

    def select_league(self):
        self.page.type(self.league_dropdown, "GO Battle League (Great)", delay=5)

    def click_battle(self):
        self.page.click(self.battle_button)
        return BattlePage(self.page)

    def click_add_selected_pokemon(self):
        self.page.click(self.add_selected_pokemon_button)

    def click_add_a_pokemon(self):
        self.page.click(self.add_pokemon_button)

    def select_pokemon(self, pokemon_list):
        for pokemon in pokemon_list:
            self.page.type(self.search_text_field, f"{pokemon}", delay=5)

    def select_difficulty(self):
        difficulty_list = [
            "Novice",
            # "Rival",
            # "Elite",
            # "Champion"
        ]
        self.page.type(self.difficulty_dropdown, random.choice(difficulty_list), delay=5)
