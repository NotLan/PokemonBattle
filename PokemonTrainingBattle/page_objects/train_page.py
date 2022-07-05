from ottermation.plugins.playwright import AbstractPage


class TrainPage(AbstractPage):

    url = 'train/'

    add_pokemon_button = 'text=+ Add Pokemon >> nth=0'
    search_text_field = 'text=Random Swap Select a Pokemon AbomasnowAbomasnow (Mega)Abomasnow (Shadow)AbraAbra >> [placeholder="Search name"]'
    pick_pokemon_dropdown = 'text=Random Swap Select a Pokemon AbomasnowAbomasnow (Mega)Abomasnow (Shadow)AbraAbra >> [placeholder="Search name"]'

    save_button = '.save-poke'
    battle_button = 'button:has-text("Battle")'

    league_dropdown = '.league-cup-select'

    opponent_pokemon_info = '.pokemon-container.opponent'
    opponent_pokemon_health = '.pokemon-container.opponent > .hp > div:nth-child(2)'

    my_pokemon_info = '.pokemon-container.self'
    my_pokemon_health = '.pokemon-container > .hp > div:nth-child(2) >> nth=0'

    shield_protection = 'text=Attack incoming! Use Protect Shield? Not Now >> div >> nth=0'
    auto_tap_button = 'text=Autotap >> nth=1'

    def pull_opponents_health(self) -> str:
        return self.page.get_attribute(self.opponent_pokemon_health, "style")

    def pull_my_health(self) -> str:
        self.page.get_attribute(self.my_pokemon_health, "style")

    def click_auto_tap(self):
        self.page.click(self.auto_tap_button)

    def select_league(self):
        self.page.click(self.league_dropdown)
        self.page.keyboard.press("ArrowDown")
        self.page.keyboard.press("Enter")

    def click_battle(self):
        self.page.click(self.battle_button)

    def select_pokemon(self, generated_pokemon_list):
        for pokemon in generated_pokemon_list:
            self.page.(self.search_text_field, f"{pokemon}")