from time import sleep

from plugins.playwright import AbstractPage


class BattlePage(AbstractPage):

    opponent_pokemon_info = '.pokemon-container.opponent'
    opponent_pokemon_health = '.pokemon-container.opponent > .hp > div:nth-child(2)'

    my_pokemon_info = '.pokemon-container.self'
    my_pokemon_health = '.pokemon-container > .hp > div:nth-child(2) >> nth=0'
    shield_protection = 'text=Attack incoming! Use Protect Shield? Not Now >> div >> nth=0'
    rematch_button = 'text=Rematch'
    defeat_header = 'text=Defeat'
    shields = '.shields >> nth=0'
    not_now = 'text=Not Now'
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
        if not self.page.is_visible(self.shields) or shield != 0:
            sleep(10)
        else:
            self.click_shield()
            shield -= 1

    def did_we_win(self):
        while not self.page.wait_for_selector(self.rematch_button, timeout=1000):
            sleep(30)
        self.page.is_visible(self.defeat_header, timeout=1000)
