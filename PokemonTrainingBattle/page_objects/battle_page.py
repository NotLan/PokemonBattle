from ottermation.plugins.playwright import AbstractPage


class BattlePage(AbstractPage):

    opponent_pokemon_info = '.pokemon-container.opponent'
    opponent_pokemon_health = '.pokemon-container.opponent > .hp > div:nth-child(2)'

    my_pokemon_info = '.pokemon-container.self'
    my_pokemon_health = '.pokemon-container > .hp > div:nth-child(2) >> nth=0'
    shield_protection = 'text=Attack incoming! Use Protect Shield? Not Now >> div >> nth=0'


    balls = '.balls >> nth=0'

    def battle_health_stats(self):
        my_pokemon_health = self.page.get_attribute(self.my_pokemon_health, "style")
        opponent_health = self.page.get_attribute(self.opponent_pokemon_health, "style")
        return my_pokemon_health, opponent_health