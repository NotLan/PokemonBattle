from time import sleep

from ottermation.plugins.playwright import AbstractPage


class BattlePage(AbstractPage):

    opponent_pokemon_info = '.pokemon-container.opponent'
    opponent_pokemon_health = '.pokemon-container.opponent > .hp > div:nth-child(2)'

    my_pokemon_info = '.pokemon-container.self'
    my_pokemon_health = '.pokemon-container > .hp > div:nth-child(2) >> nth=0'
    shield_protection = 'text=Attack incoming! Use Protect Shield? Not Now >> div >> nth=0'
    rematch_button = 'text=Rematch'
    defeat_header = 'text=Defeat'
    shields = '.shields >> nth=0'
    balls = '.balls >> nth=0'

    def battle_health_stats(self):
        my_pokemon_health = self.page.get_attribute(self.my_pokemon_health, "style")
        opponent_health = self.page.get_attribute(self.opponent_pokemon_health, "style")
        return my_pokemon_health, opponent_health

    def click_shield(self):
        self.page.click(self.shield_protection)
        self.page.is_hidden(self.shield_protection, timeout=500000)

    def is_battle_still_occurring(self):
        shield = 3
        while self.page.is_visible(self.shields) is False:
            if self.page.is_visible(self.shield_protection):
                self.click_shield()
                shield = shield - 1

    def did_we_win(self):
        while not self.page.is_visible(self.rematch_button, timeout=1000):
            sleep(1)

        self.page.is_visible(self.defeat_header, timeout=1000)
