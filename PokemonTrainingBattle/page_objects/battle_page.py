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

    def is_battle_still_occurring(self):
        while self.page.is_visible(self.shields) is False:
            if self.page.is_visible(self.shield_protection):
                self.click_shield()

    def did_we_win(self):
        return self.page.is_visible(self.defeat_header, timeout=1000)
